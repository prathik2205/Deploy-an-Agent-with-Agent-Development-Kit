"""Python function tools shared by the Paint Agent."""
from google.adk.tools import ToolContext


def set_session_value(key: str, value: str, tool_context: ToolContext) -> dict:
    """Store a key/value pair in the shared session state.

    Used by the root agent to persist SELECTED_PAINT, COVERAGE_RATE and PRICE
    so that sub-agents can read them through `{KEY?}` instruction templating.
    """
    tool_context.state[key] = value
    return {"status": f"stored '{value}' in '{key}'"}
