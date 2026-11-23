"""Calculates wall area, litres, bucket count and price for a room."""
import os

from google.adk.agents import Agent

coverage_calculator_agent = Agent(
    name="coverage_calculator_agent",
    model=os.getenv("MODEL", "gemini-2.5-flash"),
    description="Calculates paint quantity and cost from room dimensions.",
    # `{KEY?}` is ADK's optional state templating: it resolves to an empty
    # string instead of raising if the key is not yet in session state.
    instruction="""
Paint: {SELECTED_PAINT?}
Coverage rate (m2 per litre): {COVERAGE_RATE?}
Price per container: {PRICE?}

Ask for room length, width, height, number of doors and number of windows.
Wall area = 2 * (length + width) * height - 2.0 * doors - 1.5 * windows.
Report the one-coat area and ask how many coats (remember "always two coats"
preferences for later rooms). Then:
  litres  = total area / coverage rate
  buckets = ceil(litres / container size in litres)
  cost    = buckets * price per container
Present area, litres, buckets and cost. Keep a running total across rooms.
""",
)
