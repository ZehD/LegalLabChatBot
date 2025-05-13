# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY main.py .env ./

# Create directory for credentials
RUN mkdir -p /app/credentials

# Copy Google Cloud credentials
COPY service-account-key.json /app/credentials/

# Set the Google Cloud credentials environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account-key.json

# Expose port 8080
EXPOSE 8080

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]