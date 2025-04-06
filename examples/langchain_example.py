import os
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM  # Ensure langchain-ibm is installed

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables.
url = os.getenv("WATSONX_URL")
project_id = os.getenv("PROJECT_ID")
api_key = os.getenv("WATSONX_API_KEY")
# Note: The API key should be set in your environment variable 'WATSONX_APIKEY'

# Specify the model ID.
model_id = "ibm/granite-13b-instruct-v2"

# Define the model parameters.
parameters = {
    "decoding_method": "sample",   # or "greedy" if preferred
    "max_new_tokens": 200,
    "min_new_tokens": 1,
    "temperature": 0.5,
    "top_k": 50,
    "top_p": 1,
}

# Initialize the WatsonxLLM instance.
watsonx_llm = WatsonxLLM(
    model_id=model_id,
    url=url,
    project_id=project_id,
    params=parameters,
    apikey=api_key,  # Explicitly pass the API key
)

# Example of generating text.
prompt = "Write a short poem about the ocean."
response = watsonx_llm.invoke(prompt)

print(response)
