#!/bin/bash

# This script sets up the BeeAI Python environment in .venv_beeai.
echo "Setting up BeeAI environment in .venv_beeai..."

if [ -d ".venv_beeai" ]; then
    echo ".venv_beeai already exists. Activating environment..."
else
    echo "Creating virtual environment .venv_beeai..."
    python3 -m venv .venv_beeai
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create .venv_beeai. Please ensure Python 3.11 is installed."
        exit 1
    fi
fi

echo "Activating .venv_beeai..."
source .venv_beeai/bin/activate

echo "Upgrading pip in BeeAI environment..."
pip install --upgrade pip

if [ -f "requirements_beeai.txt" ]; then
    echo "Installing BeeAI dependencies from requirements_beeai.txt..."
    pip install -r requirements_beeai.txt
else
    echo "requirements_beeai.txt not found. Skipping dependency installation for BeeAI."
fi

echo "BeeAI environment setup complete."
