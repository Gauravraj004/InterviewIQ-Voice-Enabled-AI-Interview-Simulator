# Use an official Python runtime as a parent image
FROM python:3.10-slim

# INSTALL SYSTEM DEPENDENCIES
RUN apt-get update && apt-get install -y \
    gcc \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Add a non-root user for security
RUN useradd -m appuser
USER appuser

# ADD THE USER'S LOCAL BIN DIRECTORY TO THE PATH
# This is the fix for the 'gunicorn: not found' error
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application's code
COPY . .

# Make port 7860 available to the world outside this container
EXPOSE 7860

# Run app.py when the container launches
# Use gunicorn as it's a production-ready server
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
