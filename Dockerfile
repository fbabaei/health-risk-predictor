# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy app files
COPY . /app

# Create .streamlit directory with permissions
RUN mkdir -p /app/.streamlit && chmod -R 777 /app/.streamlit

# Create Streamlit config
RUN echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
port = 8501\n\
\n\
[logger]\n\
level = \"info\"\n\
" > /app/.streamlit/config.toml

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Force Streamlit to use our directory
ENV STREAMLIT_CONFIG_DIR=/app/.streamlit
ENV STREAMLIT_HOME=/app/.streamlit
ENV STREAMLIT_RUNTIME_DIR=/app/.streamlit
ENV STREAMLIT_SERVER_PORT=8501

# Expose the Streamlit port
EXPOSE 8501

# Start app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.serverAddress=0.0.0.0"]
