# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for pygame and audio
# Using only essential packages that are available in Debian
RUN apt-get update && apt-get install -y \
    libsdl2-mixer-2.0-0 \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libfreetype6 \
    libvorbis0a \
    libvorbisenc2 \
    libvorbisfile3 \
    libogg0 \
    libsndfile1 \
    curl \
    alsa-utils \
    pulseaudio \
    && rm -rf /var/lib/apt/lists/*

# Configure audio for container environment
ENV SDL_AUDIODRIVER=dummy
ENV PULSE_RUNTIME_PATH=/tmp/pulse-runtime

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create directories for pictures and music
RUN mkdir -p pictures music

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]