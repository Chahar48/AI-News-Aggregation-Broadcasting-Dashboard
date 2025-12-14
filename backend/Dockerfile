# ============================
# Backend Dockerfile
# ============================

FROM python:3.10-slim

# OS deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY app ./app

# Expose FastAPI port
EXPOSE 8000

# Run API server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
