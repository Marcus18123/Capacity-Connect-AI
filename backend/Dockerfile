FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for psycopg2 and bcrypt
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command is overridden in docker-compose.yml for development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
