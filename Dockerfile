FROM python:3.11.4-slim


# Set working directory
WORKDIR /app

# Copy requirement file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose new port
EXPOSE 8081

# Run on new port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]
