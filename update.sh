#!/bin/bash
# update.sh: Reinstall all packages in each virtual environment based on its requirements file.

# Declare an associative array mapping each virtual environment to its requirements file.
declare -A env_req_map
env_req_map[".venv"]="requirements.txt"
env_req_map[".venv_beeai"]="requirements_beeai.txt"
env_req_map[".venv_langflow"]="requirements_langflow.txt"
env_req_map[".venv_langraph"]="requirements_langraph.txt"
env_req_map[".venv_watsonx_sdk"]="requirements__watsonx_sdk.txt"

# Loop through each virtual environment defined in the map.
for env in "${!env_req_map[@]}"; do
    req_file="${env_req_map[$env]}"
    if [ -d "$env" ]; then
        echo "-----------------------------------------------------"
        echo "Activating environment: $env"
        source "$env/bin/activate"
        
        # Upgrade pip to ensure latest package management
        echo "Upgrading pip in environment: $env"
        pip install --upgrade pip
        
        if [ -f "$req_file" ]; then
            echo "Installing packages from $req_file in $env..."
            pip install -r "$req_file"
        else
            echo "Requirements file '$req_file' not found for environment '$env'. Skipping package installation."
        fi
        
        # Deactivate the virtual environment
        deactivate
        echo "Done updating environment: $env"
    else
        echo "Environment directory '$env' not found. Skipping."
    fi
done

echo "-----------------------------------------------------"
echo "All environments have been updated."
