import asyncio
import sys
import traceback

from beeai_framework.backend.chat import ChatModel
from beeai_framework.backend.message import UserMessage
from beeai_framework.tools.search.wikipedia import WikipediaTool
from beeai_framework.tools.weather.openmeteo import OpenMeteoTool
from beeai_framework.workflows.agent import AgentWorkflow, AgentWorkflowInput
from beeai_framework.errors import FrameworkError

async def main() -> None:
    # Initialize the Watsonx LLM using the provider's model identifier.
    # Note: The response_format parameter is not accepted, so it has been removed.
    llm = ChatModel.from_name("watsonx:granite-13b-instruct-v2")

    # Create a multi-agent workflow named "Smart Assistant".
    workflow = AgentWorkflow(name="Smart Assistant")

    # Add a Researcher agent to look up and provide information about a topic.
    workflow.add_agent(
        name="Researcher",
        role="A diligent researcher.",
        instructions="You look up and provide information about a specific topic.",
        tools=[WikipediaTool()],
        llm=llm,
    )

    # Add a WeatherForecaster agent to provide detailed weather reports.
    workflow.add_agent(
        name="WeatherForecaster",
        role="A weather reporter.",
        instructions="You provide detailed weather reports.",
        tools=[OpenMeteoTool()],
        llm=llm,
    )

    # Add a DataSynthesizer agent to combine disparate information into a coherent summary.
    workflow.add_agent(
        name="DataSynthesizer",
        role="A meticulous and creative data synthesizer",
        instructions="You can combine disparate information into a final coherent summary.",
        llm=llm,
    )

    # Define a location to use as context.
    location = "Saint-Tropez"

    # Run the workflow with sequential inputs:
    # 1. Provide a short history of the location.
    # 2. Provide a comprehensive weather summary for the location today.
    # 3. Summarize both historical and weather data.
    response = await workflow.run(
        inputs=[
            AgentWorkflowInput(
                prompt=f"Provide a short history of {location}.",
            ),
            AgentWorkflowInput(
                prompt=f"Provide a comprehensive weather summary for {location} today.",
                expected_output="Essential weather details such as chance of rain, temperature and wind. Only report information that is available.",
            ),
            AgentWorkflowInput(
                prompt=f"Summarize the historical and weather data for {location}.",
                expected_output=f"A paragraph that describes the history of {location}, followed by the current weather conditions.",
            ),
        ]
    ).on(
        "success",
        lambda data, event: print(
            f"\n-> Step '{data.step}' has been completed with the following outcome.\n\n{data.state.final_answer}"
        ),
    )

    # Print the final answer from the workflow.
    print("==== Final Answer ====")
    print(response.result.final_answer)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())
