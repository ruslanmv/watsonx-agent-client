#!/bin/bash

# Install Langflow on WSL Ubuntu 22.04 using the default Python 3 and a local pyproject.toml

echo "Starting Langflow installation..."

########################################
# Step 1: (Optional) Upgrade pip system-wide or for the user
########################################
echo "Step 1: Upgrading pip (system default python3)..."
python3 -m pip install --upgrade pip --user

########################################
# Step 2: Install uv (optional, if you still want uv)
########################################
echo "Step 2: Installing uv..."
python3 -m pip install uv --user

########################################
# Step 3: Create a virtual environment in the current directory
########################################
ENV_NAME=".venv_langflow"
echo "Step 3: Creating a virtual environment named $ENV_NAME..."
python3 -m venv "$ENV_NAME"
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to create virtual environment '$ENV_NAME'."
    echo "    Ensure that 'python3-venv' is installed, e.g., 'sudo apt install python3-venv'."
    exit 1
fi

########################################
# Step 4: Activate the virtual environment
########################################
echo "Step 4: Activating $ENV_NAME..."
source "$ENV_NAME"/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to activate virtual environment '$ENV_NAME'."
    exit 1
fi
echo "✅ Activated $ENV_NAME"

########################################
# Step 5: Upgrade pip inside the virtual environment
########################################
echo "Step 5: Upgrading pip inside the virtual environment..."
pip install --upgrade pip

########################################
# Step 6: Check for pyproject.toml in the current directory
########################################
echo "Step 6: Checking for pyproject.toml in the current directory..."
if [ -f "./pyproject.toml" ]; then
    echo "pyproject.toml found."
else
    echo "⚠️ pyproject.toml not found in the current directory. Please ensure this file is here."
    deactivate
    exit 1
fi

########################################
# Step 7: Install dependencies from pyproject.toml
#         (using standard pip install, avoids uv workspace errors)
########################################
echo "Step 7: Installing dependencies from pyproject.toml..."
# This assumes your pyproject.toml is properly set up for a PEP 621 style install:
# [build-system]
# requires = ["setuptools", "wheel"]
# [project]
# name = "langflow"
# ...

pip install .  # Installs the current directory as a package, reading pyproject.toml

########################################
# Step 8: Verify Langflow installation
########################################
echo "Step 8: Verifying Langflow installation..."
python -c "import langflow" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Langflow installed successfully!"
else
    echo "⚠️ Langflow installation might have issues. Check the output above."
fi

########################################
# Final Message
########################################
echo "Installation complete. You can now run Langflow."
echo "To run Langflow, activate the environment and use 'langflow run', for example:"
echo "   source $ENV_NAME/bin/activate"
echo "   langflow run"
echo "To deactivate the environment, simply run 'deactivate'."
echo "To reactivate the environment in the future, use: source $ENV_NAME/bin/activate"
echo "To remove the environment, run: rm -rf $ENV_NAME"