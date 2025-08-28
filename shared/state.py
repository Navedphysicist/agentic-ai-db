"""
Simplified state management for the Agentic AI DB system.
Only essential fields, simple dict-based state.
"""


def create_initial_state():
    return {
        "status": "initialized",
        "source_type": None,
        "dataset_id": None,
        "df": None,
        "schema": None,
        "error": None
    }


def update_state(state, **updates):
    """Update state with new values."""
    state.update(updates)
    return state


def get_status_summary(state):
    if state.get('error'):
        return f"Error: {state['error']}"

    status_parts = []

    if state.get('status'):
        status_parts.append(f"Status: {state['status']}")
    if state.get('source_type'):
        status_parts.append(f"Source: {state['source_type']}")
    if state.get('dataset_id'):
        status_parts.append(f"Dataset: {state['dataset_id']}")
    if state.get('df') is not None:
        status_parts.append(f"Data: {state['df'].shape[0]} rows")

    return " | ".join(status_parts) if status_parts else "No data loaded"
