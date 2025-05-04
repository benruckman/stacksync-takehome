# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies for nsjail and your app
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    g++ \
    make \
    flex \
    bison \
    libprotobuf-dev \
    libnl-route-3-dev \
    protobuf-compiler \
    pkg-config \
    libcap-dev \
    libseccomp-dev \
    libprotobuf-c-dev \
    zlib1g-dev \
    curl \
    build-essential \
    python3-dev \
    python3-pip && \
    pip install --no-cache-dir flask pandas && \
    # Clone and build nsjail
    git clone https://github.com/google/nsjail && \
    cd nsjail && make -j && cp nsjail /usr/local/bin/ && cd .. && rm -rf nsjail && \
    apt-get remove --purge -y git gcc g++ make flex && \
    apt-get autoremove -y && \
    apt-get clean

# Copy your app code into the container
COPY . .

# Expose Flask app on port 8080
EXPOSE 8080

# Set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Start the Flask server
CMD ["flask", "run"]