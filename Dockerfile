FROM python:3.11-slim

# Set environment variables
ENV TG_BOT_TOKEN='' \
    SAUCENAO_TOKEN=''

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the source code to the container
COPY . .

# Start the application
CMD ["python", "main.py"]
