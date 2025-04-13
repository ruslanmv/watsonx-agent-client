#!/bin/bash

# This script sets up the Langflow Python environment in .venv_langflow.
echo "Setting up Langflow environment in .venv_langflow..."

if [ -d ".venv_langflow" ]; then
    echo ".venv_langflow already exists. Activating environment..."
else
    echo "Creating virtual environment .venv_langflow..."
    python3 -m venv .venv_langflow
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create .venv_langflow. Please ensure Python 3.11 is installed."
        exit 1
    fi
fi

echo "Activating .venv_langflow..."
source .venv_langflow/bin/activate

echo "Upgrading pip in Langflow environment..."
pip install --upgrade pip

if [ -f "requirements__langflow.txt" ]; then
    echo "Installing Langflow dependencies from requirements__langflow.txt..."
    pip install -r requirements__langflow.txt
else
    echo "requirements__langflow.txt not found. Skipping dependency installation for Langflow."
fi

echo "Langflow environment setup complete."
