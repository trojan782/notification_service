# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Ensure environment variables are loaded
COPY .env /app/.env

# Make port 80 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", ""]
CMD [ "uvicorn", "main:app", "--reload" ]

