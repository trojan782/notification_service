# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip install awscli

# Copy the rest of the application code into the container at /app
COPY . .

# Set environment variables if needed (e.g., AWS credentials, region)
# ENV AWS_ACCESS_KEY_ID your_access_key
# ENV AWS_SECRET_ACCESS_KEY your_secret_key
# ENV AWS_DEFAULT_REGION your_region

# Run the application
CMD ["python3", "consumer.py"]
