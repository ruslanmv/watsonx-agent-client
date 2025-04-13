#!/bin/bash

# Activate the base environment so that run.py is executed from there.
if [ -d ".venv" ]; then
    echo "Activating base virtual environment (.venv)..."
    source .venv/bin/activate
else
    echo "ERROR: Base virtual environment (.venv) not found. Please run install.sh first."
    exit 1
fi

# Run the test harness script run.py
echo "Starting run.py to test all examples..."
python run.py

# Optionally, deactivate the virtual environment when done.
deactivate

echo "Done running all examples."
echo "You can now run the examples in the respective virtual environments."