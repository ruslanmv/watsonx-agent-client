#!/bin/bash

# This script sets up the Langraph Python environment in .venv_langraph.
echo "Setting up Langraph environment in .venv_langraph..."

if [ -d ".venv_langraph" ]; then
    echo ".venv_langraph already exists. Activating environment..."
else
    echo "Creating virtual environment .venv_langraph..."
    python3 -m venv .venv_langraph
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create .venv_langraph. Please ensure Python 3.11 is installed."
        exit 1
    fi
fi

echo "Activating .venv_langraph..."
source .venv_langraph/bin/activate

echo "Upgrading pip in Langraph environment..."
pip install --upgrade pip

if [ -f "requirements_langraph.txt" ]; then
    echo "Installing Langraph dependencies from requirements_langraph.txt..."
    pip install -r requirements_langraph.txt
else
    echo "requirements_langraph.txt not found. Skipping dependency installation for Langraph."
fi

echo "Langraph environment setup complete."
