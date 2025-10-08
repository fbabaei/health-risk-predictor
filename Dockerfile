# Use official Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy app files
COPY . /app

# Create .streamlit config folder inside /app (writeable)
RUN mkdir -p /app/.streamlit

# Configure Streamlit
RUN echo "[server]\nheadless = true\nenableCORS = false\nenableXsrfProtection = false\nport = 8501\n" > /app/.streamlit/config.toml

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8501

# ✅ Fix: Set HOME to /app so Streamlit writes configs in /app/.streamlit
ENV HOME=/app
ENV STREAMLIT_SERVER_PORT=8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Start app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
