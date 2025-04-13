# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set environment to non-interactive to avoid prompts during package installation.
ENV DEBIAN_FRONTEND=noninteractive

# Install general dependencies including curl, sudo, and software-properties-common.
RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    sudo \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Add the deadsnakes PPA to install Python 3.11 and install it along with venv and required modules.
RUN add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-venv python3.11-distutils python3-apt

# Install pip for Python 3.11 using get-pip.py.
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Set working directory
WORKDIR /app

# Copy all project files into the container.
COPY . /app

# Ensure all shell scripts are executable.
RUN chmod +x install.sh

# Run the base install script which creates .venv (base) and triggers the installation
# of all separate framework environments.
RUN ./install.sh

# Expose the port used by the Flask web app (default is 5000).
EXPOSE 5000

# Set default command to run the main web application using the base virtual environment.
CMD ["/app/.venv/bin/python", "main.py"]
