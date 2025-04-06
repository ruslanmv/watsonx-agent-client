"""
watsonx_embeddings.py

This module provides a class for generating embeddings using IBM Watsonx AI.
It leverages the official IBM Watsonx AI SDK to call the embeddings endpoint.
Ensure that you have configured your .env file with your IBM Cloud credentials.
"""

import os
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient, Credentials

class WatsonxEmbeddings:
    def __init__(self, model_id="ibm/watsonx-embedding-model", max_tokens=512):
        """
        Initialize the WatsonxEmbeddings instance.

        :param model_id: The ID of the Watsonx embeddings model.
        :param max_tokens: Maximum tokens to use for embedding generation.
        """
        load_dotenv()
        self.api_key = os.getenv("IBM_CLOUD_API_KEY")
        self.url = os.getenv("IBM_CLOUD_URL")
        self.project_id = os.getenv("IBM_CLOUD_PROJECT_ID")
        self.model_id = model_id
        self.max_tokens = max_tokens
        self.client = self._initialize_client()
    
    def _initialize_client(self):
        """
        Initialize the IBM Watsonx API client using credentials from environment variables.
        """
        credentials = Credentials(url=self.url, token=self.api_key)
        client = APIClient(credentials, project_id=self.project_id)
        return client
    
    def get_embeddings(self, text):
        """
        Generate embeddings for the given text input.

        :param text: The input text for which to generate embeddings.
        :return: The embeddings result returned by the Watsonx API.
        """
        inputs = [text]
        parameters = {
            "max_tokens": self.max_tokens
        }
        try:
            # This call assumes the embeddings endpoint is available under foundation_models.
            # Adjust the endpoint if IBM Watsonx AI provides a dedicated embeddings API.
            result = self.client.foundation_models.model(
                model=self.model_id,
                inputs=inputs,
                parameters=parameters
            ).result()
            return result
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return None

# Example usage
if __name__ == "__main__":
    sample_text = "This is a test sentence for embedding generation."
    embedder = WatsonxEmbeddings()
    embeddings = embedder.get_embeddings(sample_text)
    print("Embeddings result:")
    print(embeddings)
