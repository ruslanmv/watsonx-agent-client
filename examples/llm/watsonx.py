from langflow.base.models.model import LCModelComponent
from langflow.field_typing import LanguageModel
from langchain_ibm import ChatWatsonx
from pydantic.v1 import SecretStr
from typing import Any

import requests
from langflow.inputs import DropdownInput, IntInput, SecretStrInput, StrInput, BoolInput, SliderInput
from langflow.field_typing.range_spec import RangeSpec
from langflow.schema.dotdict import dotdict

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WatsonxLLM(LCModelComponent):
    display_name = "IBM watsonx.ai"
    description = "Generate text using IBM watsonx.ai foundation models."
    beta = False

    _default_models = ["ibm/granite-3-2b-instruct", "ibm/granite-3-8b-instruct", "ibm/granite-13b-instruct-v2"]

    inputs = [
        *LCModelComponent._base_inputs,
        DropdownInput(
            name="url",
            display_name="watsonx API Endpoint",
            info="The base URL of the API.",
            value=None,
            options=[
                "https://us-south.ml.cloud.ibm.com",
                "https://eu-de.ml.cloud.ibm.com",
                "https://eu-gb.ml.cloud.ibm.com",
                "https://au-syd.ml.cloud.ibm.com",
                "https://jp-tok.ml.cloud.ibm.com",
                "https://ca-tor.ml.cloud.ibm.com",
            ],
            real_time_refresh=True,
        ),
        StrInput(
            name="project_id",
            display_name="watsonx Project ID",
        ),
        SecretStrInput(
            name="api_key",
            display_name="API Key",
            info="The API Key to use for the model.",
            required=True,
        ),
        DropdownInput(
            name="model_name",
            display_name="Model Name",
            options=[],
            value=None,
            dynamic=True,
            required=True,
        ),
        IntInput(
            name="max_tokens",
            display_name="Max Tokens",
            advanced=True,
            info="The maximum number of tokens to generate.",
            range_spec=RangeSpec(min=1, max=4096),
            value=1000,
        ),
        StrInput(
            name="stop_sequence",
            display_name="Stop Sequence",
            advanced=True,
            info="Sequence where generation should stop.",
            field_type="str",
        ),
        SliderInput(
            name="temperature",
            display_name="Temperature",
            info="Controls randomness, higher values increase diversity.",
            value=0.1,
            range_spec=RangeSpec(min=0, max=2, step=0.01),
            advanced=True,
        ),
        SliderInput(
            name="top_p",
            display_name="Top P",
            info="The cumulative probability cutoff for token selection. Lower values mean sampling from a smaller, more top-weighted nucleus.",
            value=0.9,
            range_spec=RangeSpec(min=0, max=1, step=0.01),
            advanced=True,
        ),
        SliderInput(
            name="frequency_penalty",
            display_name="Frequency Penalty",
            info="Penalty for frequency of token usage.",
            value=0.5,
            range_spec=RangeSpec(min=-2.0, max=2.0, step=0.01),
            advanced=True,
        ),
        SliderInput(
            name="presence_penalty",
            display_name="Presence Penalty",
            info="Penalty for token presence in prior text.",
            value=0.3,
            range_spec=RangeSpec(min=-2.0, max=2.0, step=0.01),
            advanced=True,
        ),
        IntInput(
            name="seed",
            display_name="Random Seed",
            advanced=True,
            info="The random seed for the model.",
            value=8,
        ),
        BoolInput(
            name="logprobs",
            display_name="Log Probabilities",
            advanced=True,
            info="Whether to return log probabilities of the output tokens.",
            value=True,
        ),
        IntInput(
            name="top_logprobs",
            display_name="Top Log Probabilities",
            advanced=True,
            info="Number of most likely tokens to return at each position.",
            value=3,
            range_spec=RangeSpec(min=1, max=20),
        ),
    ]

    @staticmethod
    def fetch_models(base_url: str) -> list[str]:
        """Fetch available models from the watsonx.ai API."""
        try:
            endpoint = f"{base_url}/ml/v1/foundation_model_specs"
            params = {"version": "2024-09-16", "filters": "function_text_chat,!lifecycle_withdrawn"}
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            models = [model["model_id"] for model in data.get("resources", [])]
            return sorted(models)
        except Exception:
            logger.exception("Error fetching models. Using default models.")
            return WatsonxLLM._default_models

    def update_build_config(self, build_config: dotdict, field_value: Any, field_name: str | None = None):
        """Update model options when URL or API key changes."""
        logger.info("Updating build config. Field name: %s, Field value: %s", field_name, field_value)

        if field_name == "url" and field_value:
            try:
                models = self.fetch_models(base_url=build_config.url.value)
                build_config.model_name.options = models
                if build_config.model_name.value:
                    build_config.model_name.value = models[0]
                info_message = f"Updated model options: {len(models)} models found in {build_config.url.value}"
                logger.info(info_message)
            except Exception:
                logger.exception("Error updating model options.")

    def build_model(self) -> LanguageModel:
        chat_params = {
            "max_tokens": getattr(self, "max_tokens", None),
            "temperature": getattr(self, "temperature", None),
            "top_p": getattr(self, "top_p", None),
            "frequency_penalty": getattr(self, "frequency_penalty", None),
            "presence_penalty": getattr(self, "presence_penalty", None),
            "seed": getattr(self, "seed", None),
            "stop": [self.stop_sequence] if self.stop_sequence else [],
            "n": 1,
            "logprobs": getattr(self, "logprobs", True),
            "top_logprobs": getattr(self, "top_logprobs", None),
            "time_limit": 600000,
            "logit_bias": {"1003": -100, "1004": -100},
        }
        # Force the API key to use a Bearer token.
        raw_key = SecretStr(self.api_key).get_secret_value().strip()
        if not raw_key.startswith("Bearer "):
            token = "Bearer " + raw_key
        else:
            token = raw_key

        return ChatWatsonx(
            apikey=token,
            url=self.url,
            project_id=self.project_id,
            model_id=self.model_name,
            params=chat_params,
            streaming=self.stream,
        )

    def generate_text(self, prompt: str) -> str:
        """
        Generate text using the built model.
        """
        try:
            llm_instance = self.build_model()
            # Assuming ChatWatsonx instance is callable with a prompt.
            response = llm_instance(prompt)
            return response
        except Exception as e:
            return f"Error generating text: {e}"


# Standalone usage example
if __name__ == "__main__":
    sample_prompt = "Explain the benefits of using Watsonx AI models in modern applications."
    # Replace the following values with valid credentials.
    import os
    from dotenv import load_dotenv

    # Load environment variables from .env file
    load_dotenv()

    api_key = os.getenv("WATSONX_API_KEY")
    url = os.getenv("WATSONX_URL")
    project_id = os.getenv("PROJECT_ID")
    llm = WatsonxLLM(
        url= url,
        project_id=project_id,
        api_key=api_key,        # your API key (without the "Bearer " prefix)
        model_name="ibm/granite-13b-instruct-v2",
        max_tokens=1000,
        stop_sequence="",
        temperature=0.1,
        top_p=0.9,
        frequency_penalty=0.5,
        presence_penalty=0.3,
        seed=8,
        logprobs=True,
        top_logprobs=3,
        stream=False,
    )
    response = llm.generate_text(sample_prompt)
    print("Generated Text:")
    print(response)
# This code is designed to be run as a standalone script for testing purposes.
# In a production environment, you would typically integrate this class into a larger application.
