#!/bin/bash

# This script sets up the base Python 3.11 environment and installs project-wide dependencies.
# It also triggers installation scripts for individual framework environments.

echo "🔧 Adding deadsnakes PPA and updating packages..."
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

echo "🐍 Installing Python 3.11 and required packages..."
sudo apt install -y python3.11 python3.11-venv python3.11-distutils

echo "🛠️ Fixing apt_pkg issues by installing python3-apt..."
sudo apt install -y python3-apt

echo "⚙️ Setting Python 3.11 as the default python3..."
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 2
sudo update-alternatives --config python3

echo "💡 Installing pip for Python 3.11..."
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.11

echo "✅ Python version after setup:"
python3 --version
python3 -m pip --version

# Set up the base virtual environment (.venv)
if [ -d ".venv" ]; then
    echo ".venv already exists. Activating the base virtual environment..."
else
    echo "Creating base virtual environment (.venv)..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to create .venv. Please ensure Python 3.11 is properly installed."
        exit 1
    fi
fi

echo "Activating base virtual environment..."
source .venv/bin/activate

echo "⬆️ Upgrading pip in base environment..."
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    echo "📦 Installing base dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "📄 requirements.txt not found. Skipping base dependency installation."
fi

echo "🎉 Base environment setup is complete."

# Now trigger installation of individual framework environments
echo "🚀 Setting up individual framework environments..."
bash install_beeai.sh
bash install_langflow.sh
bash install_watsonx_sdk.sh
bash install_langraph.sh

echo "🎉 All environments have been set up."
