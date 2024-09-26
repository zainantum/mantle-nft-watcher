# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV scraper_module=a7df32de3a60dfdb7a0b
ENV PYTHON_VERSION=3.10.11
ENV PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/0d8570dc44796f4369b652222cf176b3db6ac70e/public/get-pip.py
ENV PYTHON_GET_PIP_SHA256=96461deced5c2a487ddc65207ec5a9cffeca0d34e7af7ea1afc470ff0d746207
ENV PYTHON_SETUPTOOLS_VERSION=65.5.1
ENV PYTHON_PIP_VERSION=23.0.1
ENV LANG=C.UTF-8
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Copy the application code
COPY ./src /app

# Install system dependencies and set up the Python environment
RUN apt-get update && apt-get install -y \
    git \
    mercurial \
    openssh-client \
    subversion \
    procps \
    ca-certificates \
    curl \
    gnupg \
    netbase \
    wget \
    chromium \
    chromium-driver \
    xvfb \
    libbluetooth-dev \
    tk-dev \
    uuid-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade "git+https://github.com/exorde-labs/${scraper_module}" \
    && pip install --no-cache-dir pandas aioprometheus==23.3.0 opentelemetry-api opentelemetry-sdk \
    opentelemetry-exporter-jaeger opentelemetry-instrumentation-aiohttp-client opentelemetry-sdk \
    opentelemetry-exporter-otlp

# Set up symbolic links for Python binaries
RUN set -eux; \
    ln -svT /usr/local/bin/python3 /usr/local/bin/python; \
    ln -svT /usr/local/bin/pip3 /usr/local/bin/pip

# Install additional Python packages
RUN wget -O get-pip.py "$PYTHON_GET_PIP_URL" && \
    echo "$PYTHON_GET_PIP_SHA256 *get-pip.py" | sha256sum -c - && \
    python get-pip.py --disable-pip-version-check --no-cache-dir --no-compile "pip==$PYTHON_PIP_VERSION" "setuptools==$PYTHON_SETUPTOOLS_VERSION" && \
    rm -f get-pip.py && \
    pip --version

# Ensure the Python environment is clean
RUN find /usr/local -depth \( \
        \( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
        -o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' -o -name 'libpython*.a' \) \) \
    \) -exec rm -rf '{}' +

# Expose any required ports (optional, based on your application's needs)
# EXPOSE 8080

# Define the entry point and default command
ENTRYPOINT ["python3.10", "/app/scraper.py"]

# Optionally add CMD if needed for different behavior
CMD ["bash"]
