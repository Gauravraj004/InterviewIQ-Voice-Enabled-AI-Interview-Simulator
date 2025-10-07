import os
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint, HuggingFaceEmbeddings
import speech_creator
from dotenv import load_dotenv
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Cassandra
import cassio

# Load environment variables at module level (for deployed environments)
load_dotenv()

# Global store for chat histories (session_id -> ChatMessageHistory)
_chat_sessions = {}

# Global store for resume RAG retrievers (session_id -> retriever)
_resume_retrievers = {}

def get_chat_history(session_id: str = "default"):
    """Get or create chat history for a session."""
    if session_id not in _chat_sessions:
        _chat_sessions[session_id] = ChatMessageHistory()
    return _chat_sessions[session_id]

def clear_chat_history(session_id: str = "default"):
    """Clear chat history for a session."""
    if session_id in _chat_sessions:
        del _chat_sessions[session_id]
    return True

def reset_resume_table(table_name: str):
    """
    Reset (drop) the Astra DB table for resume data.
    This clears all previous resume chunks stored for this session.
    Uses direct CQL query for reliable cleanup.
    
    Args:
        table_name: Name of the Astra DB table to drop
    
    Returns:
        bool: True if successful or table doesn't exist, False on error
    """
    try:
        # Get session using cassio's config API
        from cassio.config import check_resolve_session, check_resolve_keyspace
        
        session = check_resolve_session()
        keyspace = check_resolve_keyspace()
        
        if not session or not keyspace:
            print(f"[WARN] Cassio not initialized, cannot drop table '{table_name}'")
            return False
        
        # Use DROP TABLE IF EXISTS for safe cleanup
        drop_query = f"DROP TABLE IF EXISTS {keyspace}.{table_name};"
        print(f"[INFO] Dropping table '{table_name}' from keyspace '{keyspace}'...")
        session.execute(drop_query)
        print(f"[INFO] Table '{table_name}' dropped successfully (or didn't exist).")
        return True
        
    except Exception as e:
        print(f"[WARN] Could not drop table '{table_name}': {e}")
        # Not critical - table might not exist or might be in use
        return False


def cleanup_all_resume_tables():
    """
    Cleanup all resume-related tables on server startup.
    Drops all tables matching pattern 'resume_*'.
    This ensures a fresh start without stale data.
    
    Returns:
        int: Number of tables successfully dropped
    """
    try:
        # Load Astra DB credentials from environment
        astra_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
        astra_db_id = os.getenv("ASTRA_DB_ID")
        
        if not astra_token or not astra_db_id:
            print("[WARN] Astra DB credentials not found, skipping cleanup")
            return 0
        
        # Initialize cassio connection
        cassio.init(token=astra_token, database_id=astra_db_id)
        print("[INFO] Connected to Astra DB for cleanup")
        
        # Get session using cassio's config
        from cassio.config import check_resolve_session, check_resolve_keyspace
        session = check_resolve_session()
        keyspace = check_resolve_keyspace()
        
        if not session or not keyspace:
            print("[WARN] Could not resolve cassio session/keyspace")
            return 0
        
        # Query all tables in keyspace
        query = f"SELECT table_name FROM system_schema.tables WHERE keyspace_name = '{keyspace}';"
        rows = session.execute(query)
        
        # Filter and drop resume tables
        dropped_count = 0
        for row in rows:
            table_name = row.table_name
            if table_name.startswith('resume_'):
                try:
                    drop_query = f"DROP TABLE IF EXISTS {keyspace}.{table_name};"
                    session.execute(drop_query)
                    print(f"[INFO] Dropped table: {table_name}")
                    dropped_count += 1
                except Exception as e:
                    print(f"[WARN] Could not drop {table_name}: {e}")
        
        if dropped_count > 0:
            print(f"[INFO] Cleanup complete: {dropped_count} resume table(s) dropped")
        else:
            print("[INFO] No resume tables found to clean up")
        
        return dropped_count
        
    except Exception as e:
        print(f"[ERROR] Cleanup failed: {e}")
        import traceback
        traceback.print_exc()
        return 0

def setup_resume_rag_from_bytes(pdf_bytes, filename: str, session_id: str = "default", reset_table: bool = True):
    """
    Load and process resume PDF from memory (BytesIO), create Astra DB vector store and retriever.
    NO LOCAL FILE STORAGE - Everything goes directly to Astra DB.
    
    Args:
        pdf_bytes: BytesIO object containing PDF data
        filename: Original filename for reference
        session_id: Session ID to associate the retriever with
        reset_table: If True, drops the existing table before creating new one (default: True)
    """
    try:
        from pypdf import PdfReader
        from langchain.schema import Document
        
        # Load Astra DB credentials from environment variables
        astra_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
        astra_db_id = os.getenv("ASTRA_DB_ID")
        if not astra_token or not astra_db_id:
            raise ValueError("Astra DB credentials not found. Please set ASTRA_DB_APPLICATION_TOKEN and ASTRA_DB_ID in Hugging Face Space Secrets.")
        
        # Check for HuggingFace token (needed for embeddings)
        # HF token can come from either UI (set via /set_api) or environment
        hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        if not hf_token:
            raise ValueError("⚠️ Please provide your HuggingFace API key in the sidebar first!")
        print(f"[INFO] Loading PDF from memory: {filename}")
        
        # Read PDF from BytesIO object
        pdf_reader = PdfReader(pdf_bytes)
        documents = []
        for i, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            documents.append(Document(
                page_content=text,
                metadata={"source": filename, "page": i}
            ))
        print(f"[INFO] Loaded {len(documents)} pages from PDF")
        
        # Initialize Cassandra/Astra DB connection
        cassio.init(token=astra_token, database_id=astra_db_id)
        print("[INFO] Connected to Astra DB")
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)
        print(f"[INFO] Split into {len(splits)} chunks")
        # Create embeddings (runs locally, FREE!)
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",  # Faster, smaller model
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        print("[INFO] Embeddings model loaded")
        # Create Astra DB vector store
        table_name = f"resume_{session_id.replace('-', '_')}"  # Table names can't have dashes
        
        # Reset table if requested (clears old resume data)
        if reset_table:
            print(f"[INFO] Resetting table '{table_name}' to clear old resume data...")
            reset_resume_table(table_name)
        
        print(f"[INFO] Creating vector store in Astra DB table: {table_name}")
        vectorstore = Cassandra(
            embedding=embeddings,
            table_name=table_name,
            session=None,  # Uses cassio session
            keyspace=None,  # Uses default keyspace
        )
        # Add documents to vector store
        print("[INFO] Adding documents to Astra DB...")
        vectorstore.add_documents(splits)
        print(f"[INFO] Successfully stored {len(splits)} chunks in Astra DB")
        # Create retriever
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        # Store retriever for this session
        _resume_retrievers[session_id] = retriever
        print("[INFO] Resume RAG setup complete!")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to setup resume RAG with Astra DB: {e}")
        import traceback
        traceback.print_exc()
        return False




def chat_with_history(user_message: str, session_id: str = "default", use_resume: bool = False):
    """
    Send a message and get a response with conversation history.
    
    Args:
        user_message: The user's message
        session_id: Session ID to track conversation history
        use_resume: Whether to use resume context for answers
    
    Returns:
        AI response string
    """
    # Get chat history for this session
    history = get_chat_history(session_id)
    
    # Build context from resume if requested and available
    resume_context = ""
    if use_resume and session_id in _resume_retrievers:
        try:
            retriever = _resume_retrievers[session_id]
            docs = retriever.get_relevant_documents(user_message)
            resume_context = "\n\nResume Context:\n" + "\n".join([doc.page_content for doc in docs])
        except Exception as e:
            print(f"Error retrieving resume context: {e}")
    
    # Add system message if this is a new conversation
    if len(history.messages) == 0:
        system_content = """You are an experienced interviewer conducting a realistic interview. 
                            Your goal is to engage in a natural, human-like conversation — not rigid question-answering. 
                            Act as a professional interviewer who asks follow-up questions, comments on responses, and adapts naturally like a real person would. 

                            Interview Flow:
                            1. Start with a warm introduction and small talk to make the candidate comfortable. 
                            2. Ask the candidate to introduce themselves. 
                            . If a resume or profile data is available in the retriever/uploaded document:
                               - Refer to it naturally during conversation (e.g., “I see you’ve worked on X, could you tell me more about that?”).
                               - Use resume details to ask specific, contextual, and open-ended questions. 
                               - Explore both technical/project aspects and soft skills/leadership elements. 
                            4. If no resume is available:
                               - Conduct a generic interview, starting with background, education, projects, and interests. 
                            5. Ask one question at a time, allowing space for the candidate to respond before continuing. 
                            6. Vary tone between formal and conversational to feel like a real person. 
                            7. Encourage storytelling and elaboration by asking “why” and “how” follow-ups. 
                            8. Gradually move from personal introduction → resume/project discussion → technical/behavioral questions → wrap-up.
                            9. Close with polite remarks and next steps, just like a real interview. 
                            
                            Rules:
                            - Stay professional yet approachable. 
                            - Do not dump a list of questions; always ask naturally in flow. 
                            - If candidate gives very short answers, probe deeper politely. 
                            - If resume info is present, prioritize it. If not, proceed generally. 
                            - Never break the interviewer role. Always sound like a human interviewer. 
                            - Keep responses small but engaging.
                            - Do not write more than 50 words in a single response.
                            """
        if use_resume:
            system_content += " Use the candidate's resume information when it's provided to ask relevant, personalized questions."
        system_msg = SystemMessage(content=system_content)
        history.add_message(system_msg)
    
    # Add user message with resume context if available
    user_msg_content = user_message
    if resume_context:
        user_msg_content += resume_context
    
    history.add_user_message(user_msg_content)
    
    # Get all messages for context
    all_messages = history.messages
    
    # Use HuggingFace endpoint - token already set in environment by /set_api
    llm = HuggingFaceEndpoint(
        repo_id="openai/gpt-oss-120b",
        task="conversational",
        max_new_tokens=512,
        do_sample=False,
        repetition_penalty=1.03,
        provider="auto",
    )
    chat_model = ChatHuggingFace(llm=llm)
    response = chat_model.invoke(all_messages)
    ai_response = response.content
    
    # Add AI response to history
    history.add_ai_message(ai_response)
    
    return ai_response


def run_interview_assistant():
    """Run the voice-based interview assistant with history."""
    # Don't load from .env - API key should be set via environment
    # load_dotenv()  # REMOVED
    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not hf_token:
        print("⚠️ No HuggingFace API key found!")
        print("Get your key from: https://huggingface.co/settings/tokens")
        print("Set it in the web interface or as environment variable")
        return
    
    session_id = "voice_interview"
    exit_phrase = "thank you"
    
    print("Interview assistant started. Say 'thank you' to exit.")
    
    while True:
        try:
            user_input = speech_creator.get_transcribed_text()
            print(f"You: {user_input}")
        except Exception as e:
            print("Sorry, I could not understand your speech. Please try again.")
            continue
        
        if user_input.strip().lower() == exit_phrase:
            print("Interview session ended.")
            break
        
        # Use history-aware chat
        response = chat_with_history(user_input, session_id)
        print(f"AI: {response}")