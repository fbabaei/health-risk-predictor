# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Create .streamlit directory inside the app folder
RUN mkdir -p /app/.streamlit

# Add Streamlit config
RUN echo "[server]\nheadless = true\nenableCORS = false\nenableXsrfProtection = false\nport = 8501\n" > /app/.streamlit/config.toml

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Streamlit
EXPOSE 8501

# Environment variable so Streamlit knows where to write configs
ENV STREAMLIT_HOME=/app/.streamlit
ENV STREAMLIT_SERVER_PORT=8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
