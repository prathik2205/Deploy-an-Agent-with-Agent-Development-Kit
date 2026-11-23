"""Collects colour choice per room, then delegates to the coverage calculator."""
import os

from google.adk.agents import Agent

from .sub_agents.coverage_calculator.agent import coverage_calculator_agent

room_planner_agent = Agent(
    name="room_planner_agent",
    model=os.getenv("MODEL", "gemini-2.5-flash"),
    description="Gathers rooms and colour choices for the selected paint.",
    instruction="""
Selected paint: {SELECTED_PAINT?}

For each room the customer named, ask which colour from the selected product
they want. Once a colour is chosen for a room, transfer to
coverage_calculator_agent to size that room. Remember rooms already priced.
""",
    sub_agents=[coverage_calculator_agent],
)
