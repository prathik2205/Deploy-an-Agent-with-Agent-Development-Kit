"""Isolated search agent grounded on the Agent Search data store."""
import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import VertexAiSearchTool

load_dotenv()

project = os.environ["GOOGLE_CLOUD_PROJECT"]
engine_id = os.environ["SEARCH_ENGINE_ID"]

paint_searcher_agent = Agent(
    name="paint_searcher_agent",
    model=os.getenv("MODEL", "gemini-2.5-flash"),
    description="Answers questions about Cymbal Shops paint products from the datasheet.",
    instruction=(
        "Answer only from the Cymbal Shops paint datasheet. Report product "
        "names, colours, coverage rates and prices per container."
    ),
    tools=[
        VertexAiSearchTool(
            search_engine_id=(
                f"projects/{project}/locations/global/collections/"
                f"default_collection/engines/{engine_id}"
            )
        )
    ],
)
