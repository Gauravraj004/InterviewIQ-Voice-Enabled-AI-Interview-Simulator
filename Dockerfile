# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Add a non-root user for security
RUN useradd -m appuser
USER appuser

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application's code
COPY . .

# Make port 7860 available to the world outside this container
EXPOSE 7860

# Define environment variable
ENV NAME World

# Run app.py when the container launches
# Use gunicorn as it's a production-ready server
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
