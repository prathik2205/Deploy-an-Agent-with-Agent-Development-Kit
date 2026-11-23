"""Root agent: orchestrates paint selection, room planning and cost calculation."""
import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.paint_searcher.agent import paint_searcher_agent
from .sub_agents.room_planner.agent import room_planner_agent
from .tools import set_session_value

load_dotenv()
MODEL = os.getenv("MODEL", "gemini-2.5-flash")

root_agent = Agent(
    name="paint_agent",
    model=MODEL,
    description="Helps customers choose paint, colors, quantity and total price.",
    instruction="""
You are the Paint Agent for Cymbal Shops' Paint Department.

1. Greet the customer and offer to share information about Cymbal Shops paints.
2. When they agree, use the paint search tool to summarize the four product
   lines: EcoGreens, Forever Paint, Project Paint and SureCoverage.
3. When the customer selects a product, look up its coverage rate (m2 per
   liter) and price per container, then call `set_session_value` three times
   to store SELECTED_PAINT, COVERAGE_RATE and PRICE.
4. Show the product's colour swatches and ask how many rooms they are painting
   and what each room is called.
5. Hand over to room_planner_agent for colour choice and measurements.
""",
    tools=[
        # A search tool cannot be mixed with other tools or implicit
        # transfer_to_agent calls, so the search agent is wrapped as an AgentTool.
        AgentTool(agent=paint_searcher_agent, skip_summarization=False),
        set_session_value,
    ],
    sub_agents=[room_planner_agent],
)
