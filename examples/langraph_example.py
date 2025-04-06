import os
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM  # Import from langchain_ibm
from langgraph.graph import StateGraph, END
from langchain.schema import HumanMessage

# Load environment variables from .env file
load_dotenv()

# Load API credentials and project ID from environment variables
api_key = os.getenv("WATSONX_API_KEY")
url = os.getenv("WATSONX_URL")
project_id = os.getenv("PROJECT_ID")

# Specify the model ID
model_id = "ibm/granite-13b-instruct-v2"

# Initialize the WatsonxLLM with the correct parameter names
watsonx_llm = WatsonxLLM(
    model_id=model_id,
    url=url,
    apikey=api_key,
    project_id=project_id,
    params={
        "decoding_method": "greedy",
        "max_new_tokens": 200
    }
)

# Define a node in the graph that uses the Watsonx model
def generate_response(state):
    messages = state["messages"]
    response = watsonx_llm.invoke(messages)
    return {"messages": messages + [response]}

# Create a new graph and add the node
workflow = StateGraph(dict)
workflow.add_node("generate", generate_response)
workflow.set_entry_point("generate")
workflow.add_edge("generate", END)
app = workflow.compile()

# Example usage
inputs = {"messages": [HumanMessage(content="Tell me a joke.")]}

result = app.invoke(inputs)

# Print only the answer (assumed to be the last element in the messages list)
answer = result["messages"][-1]
print(answer)
