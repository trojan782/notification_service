FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip install awscli

COPY . .

# Run the application
CMD ["python3", "consumer.py"]
