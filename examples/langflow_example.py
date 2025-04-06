"""
langflow_example.py

This example simulates how to integrate Watsonx models with Langflow.
While Langflow is typically configured through its visual interface, this
script demonstrates how you might invoke the Watsonx model backend using
the WatsonxLLM wrapper (now located in examples/llm/watsonx.py) as if it were configured
within a Langflow flow.

Ensure that you have a valid .env file with your IBM Cloud credentials.
"""

import os
from dotenv import load_dotenv

# Import WatsonxLLM from the new package location.
# Make sure that the folder 'examples/llm' contains an __init__.py file.
from llm.watsonx import WatsonxLLM

def main():
    # Load environment variables from .env
    load_dotenv()
    
    # Initialize WatsonxLLM as configured for Langflow integration.
    model_id = "ibm/granite-13b-instruct-v2"
    watsonx_llm = WatsonxLLM(
        model_id=model_id,
        decoding_method="greedy",
        max_new_tokens=200
    )
    
    # Simulate input from a Langflow flow.
    prompt = "Describe the future of artificial intelligence."
    
    # Invoke the Watsonx model and get the response.
    response = watsonx_llm.generate_text(prompt)
    
    print("Langflow simulated response:")
    print(response)

if __name__ == "__main__":
    main()
# This script is a standalone example and does not require Langflow to run.
# It demonstrates how to use the WatsonxLLM wrapper to generate text based on a prompt.