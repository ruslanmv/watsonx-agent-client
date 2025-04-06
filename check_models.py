"""
check_models.py

This script checks the integration and functionality of the Watsonx models.
It tests both the text generation and embeddings endpoints using the IBM Watsonx AI SDK.
Ensure your .env file is properly configured with your IBM Cloud credentials.
"""

import os
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient, Credentials
from embeddings.watsonx_embeddings import WatsonxEmbeddings

def initialize_client():
    """Initialize the IBM Watsonx API client using credentials from the .env file."""
    load_dotenv()  # Load credentials from .env file
    api_key = os.getenv("IBM_CLOUD_API_KEY")
    url = os.getenv("IBM_CLOUD_URL")
    project_id = os.getenv("IBM_CLOUD_PROJECT_ID")

    credentials = Credentials(url=url, token=api_key)
    client = APIClient(credentials, project_id=project_id)
    return client

def check_text_generation():
    """Test the text generation model using a sample prompt."""
    print("Checking text generation model...")
    client = initialize_client()
    model_id = "ibm/granite-13b-instruct-v2"  # Example model ID
    prompt = "Write a brief introduction about IBM Watsonx."
    parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 100
    }
    
    try:
        result = client.foundation_models.model(
            model=model_id, 
            inputs=[prompt], 
            parameters=parameters
        ).result()
        print("Text Generation Result:")
        print(result)
    except Exception as e:
        print("Error during text generation:", e)

def check_embeddings_generation():
    """Test the embeddings generation using a sample text."""
    print("Checking embeddings generation...")
    try:
        embedder = WatsonxEmbeddings(model_id="ibm/watsonx-embedding-model")
        sample_text = "IBM Watsonx provides state-of-the-art AI capabilities."
        embeddings = embedder.get_embeddings(sample_text)
        print("Embeddings Result:")
        print(embeddings)
    except Exception as e:
        print("Error during embeddings generation:", e)

if __name__ == "__main__":
    print("Starting model checks...\n")
    check_text_generation()
    print("\n")
    check_embeddings_generation()
