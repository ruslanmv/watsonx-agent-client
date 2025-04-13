import os
import subprocess
import logging

# Configure logging to output info and errors with timestamps.
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')

# List of framework example scripts to be tested.
example_files = [
    "beeai_example.py",
    "langchain_example.py",
    "langflow_example.py",
    "langraph_example.py",
    "watsonx_sdk_example.py"
]

EXAMPLES_DIR = "examples"

def select_venv(filename):
    """
    Choose the appropriate Python interpreter based on the example's filename.

    Mapping:
      - If filename contains "beeai", use the BeeAI environment (.venv_beeai).
      - If filename contains "langflow", use the Langflow environment (.venv_langflow).
      - If filename contains "watsonx_sdk", use the WatsonX SDK environment (.venv_watsonx_sdk).
      - If filename contains "langraph", use the Langraph environment (.venv_langraph).
      - Otherwise, use the base environment (.venv).

    Returns:
      The absolute path to the appropriate Python interpreter.
    """
    framework_map = {
        "beeai": ".venv_beeai",
        "langflow": ".venv_langflow",
        "watsonx_sdk": ".venv_watsonx_sdk",
        "langraph": ".venv_langraph",
    }
    for key, venv in framework_map.items():
        if key in filename:
            return os.path.join(os.getcwd(), venv, "bin", "python")
    return os.path.join(os.getcwd(), ".venv", "bin", "python")

def run_example(example_file):
    """
    Run the provided example using the appropriate virtual environment.
    Logs the output or errors accordingly.
    """
    interpreter = select_venv(example_file)
    full_path = os.path.join(os.getcwd(), EXAMPLES_DIR, example_file)
    logging.info("Running '%s' using interpreter: %s", full_path, interpreter)

    try:
        result = subprocess.run(
            [interpreter, full_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            logging.info("SUCCESS: '%s' executed successfully.", full_path)
            logging.info("Output:\n%s", result.stdout)
        else:
            logging.error("ERROR: '%s' encountered an error (return code %s).", full_path, result.returncode)
            logging.error("Error output:\n%s", result.stderr)
    except subprocess.TimeoutExpired:
        logging.error("TIMEOUT: '%s' did not complete within the timeout period.", full_path)
    except Exception as e:
        logging.exception("EXCEPTION: An error occurred while running '%s': %s", full_path, str(e))

def main():
    # Loop through each example file and run it.
    for file in example_files:
        full_path = os.path.join(os.getcwd(), EXAMPLES_DIR, file)
        if os.path.exists(full_path):
            run_example(file)
        else:
            logging.warning("File '%s' does not exist in '%s'. Skipping.", file, EXAMPLES_DIR)

if __name__ == "__main__":
    main()