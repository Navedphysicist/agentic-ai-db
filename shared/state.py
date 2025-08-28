"""
Simplified state management for the Agentic AI DB system.
Only essential fields, simple dict-based state.
"""

from typing import Dict, Any
from datetime import datetime
import uuid


def create_initial_state() -> Dict[str, Any]:
    """Create the initial state for a new data analysis session."""
    return {
        "session_id": str(uuid.uuid4()),
        "source_type": None,  # csv, sql, mongo, sheets
        "dataset_id": None,
        "df": None,  # Direct DataFrame reference (simpler)
        "schema": None,  # Simple schema (columns, types)
        "user_query": None,
        "plan_dsl": None,
        "result_df": None,
        "summary": None,
        "error": None,
        "status": "initialized"  # initialized, processing, completed, error
    }


def update_state(state: Dict[str, Any], **updates) -> Dict[str, Any]:
    """Update state with new values."""
    state.update(updates)
    return state


def get_status_summary(state: Dict[str, Any]) -> str:
    """Get a human-readable summary of the current state."""
    if state.get("error"):
        return f"Error: {state['error']}"

    if state.get("status") == "completed":
        return f"Analysis completed for {state.get('source_type', 'unknown')} dataset"

    if state.get("status") == "processing":
        return f"Processing {state.get('source_type', 'unknown')} dataset..."

    if state.get("df") is not None:
        return f"Ready to analyze {state.get('source_type', 'unknown')} dataset"

    return "Initializing..."
