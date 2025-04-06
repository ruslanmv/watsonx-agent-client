
# Langflow Integration with Watsonx Models

**Installation:**

Follow the installation instructions for Langflow. Typically, you will clone the repository and install dependencies. Additionally, install:

```bash
pip install ibm-watsonx-ai langchain python-dotenv
```

**Configuring Langflow:**

1. **Start Langflow:** Run the Langflow application.
2. **Create a New Flow:** Click on "Create Flow" in the Langflow UI.
3. **Add a WatsonxLLM Component:** Search for the WatsonxLLM component in the components panel and drag it onto the canvas.
4. **Configure the Component:** In the properties panel for the WatsonxLLM component, set the following:
    - **IBM Cloud URL:** Your Watsonx API endpoint.
    - **IBM Cloud API Key:** Your IBM Cloud API key.
    - **IBM Cloud Project ID (or Space ID):** The project or space identifier.
    - **Model ID:** For example, "ibm/granite-13b-instruct-v2".
    - **Optional Model Parameters:** Such as `decoding_method` (e.g., "greedy") and `max_new_tokens` (e.g., 200).
5. **Connect to Other Components:** Link the WatsonxLLM component to other components like a Prompt Template or Output Parser to build your workflow.
6. **Environment Variables:** Optionally, configure Langflow to load environment variables from a `.env` file if your deployment supports it.

**Running the Example Code:**

The repository includes an example Python script that simulates Langflow's integration with Watsonx models. To run this example from the root directory, follow these steps:

1. **Configure Your Environment:**  
   Ensure that your `.env` file (located at the root of the repository) is properly configured with your IBM Cloud credentials:
   ```env
   IBM_CLOUD_API_KEY="YOUR_API_KEY"
   IBM_CLOUD_URL="https://us-south.ml.cloud.ibm.com"  # Or your region's URL
   IBM_CLOUD_PROJECT_ID="YOUR_PROJECT_ID"             # Or space_id if using a space
   ```

2. **Run the Example Script:**  
   From the root directory of the repository, execute:
   ```bash
   python examples/langflow_example.py
   ```
   This script will:
   - Load your IBM Cloud credentials from the `.env` file.
   - Initialize the WatsonxLLM integration.
   - Simulate a prompt input (e.g., "Describe the future of artificial intelligence.").
   - Generate and print the response from the Watsonx model.

This updated setup enables you to both integrate Watsonx models directly within the Langflow UI and test the integration using a standalone Python example.
