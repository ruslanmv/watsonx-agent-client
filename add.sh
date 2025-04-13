#!/bin/bash

# Check for correct usage
if [ "$#" -ne 2 ] || [ "$1" != "package" ]; then
    echo "Usage: ./add.sh package <package-name>"
    exit 1
fi

PACKAGE_NAME="$2"

# List of virtual environment directories
VENV_DIRS=(
  ".venv_beeai"
  ".venv_langflow"
  ".venv_langraph"
  ".venv_watsonx_sdk"
  ".venv"
)

for VENV in "${VENV_DIRS[@]}"; do
  if [ -d "$VENV" ]; then
    echo "Activating $VENV and installing $PACKAGE_NAME..."
    source "$VENV/bin/activate"
    pip install "$PACKAGE_NAME"
    deactivate
    echo "Done with $VENV"
  else
    echo "Skipping $VENV - Directory does not exist"
  fi
done
