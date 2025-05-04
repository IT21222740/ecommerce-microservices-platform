FROM python:3.11.4-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirement file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Accept build argument for the Firebase credentials file
ARG FIREBASE_CREDENTIALS_FILE
COPY ${FIREBASE_CREDENTIALS_FILE} ./ecommerce-microservices.json

# Expose new port
EXPOSE 8081

# Run on new port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]
