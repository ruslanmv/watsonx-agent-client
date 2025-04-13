#!/bin/bash

# This script sets up the WatsonX SDK Python environment in .venv_watsonx_sdk.
echo "Setting up WatsonX SDK environment in .venv_watsonx_sdk..."

if [ -d ".venv_watsonx_sdk" ]; then
    echo ".venv_watsonx_sdk already exists. Activating environment..."
else
    echo "Creating virtual environment .venv_watsonx_sdk..."
    python3 -m venv .venv_watsonx_sdk
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create .venv_watsonx_sdk. Please ensure Python 3.11 is installed."
        exit 1
    fi
fi

echo "Activating .venv_watsonx_sdk..."
source .venv_watsonx_sdk/bin/activate

echo "Upgrading pip in WatsonX SDK environment..."
pip install --upgrade pip

if [ -f "requirements__watsonx_sdk.txt" ]; then
    echo "Installing WatsonX SDK dependencies from requirements__watsonx_sdk.txt..."
    pip install -r requirements__watsonx_sdk.txt
else
    echo "requirements__watsonx_sdk.txt not found. Skipping dependency installation for WatsonX SDK."
fi

echo "WatsonX SDK environment setup complete."
