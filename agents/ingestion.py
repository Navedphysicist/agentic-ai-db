"""
Simplified Ingestion Agent - The first agent in the pipeline.
Handles CSV file processing and basic schema inference.
"""

from typing import Dict, Any
from shared.state import update_state
from data.csv_handler import CSVHandler


class IngestionAgent:
    """
    Simple Ingestion Agent for CSV files.

    This agent:
    1. Validates CSV files
    2. Processes CSV to DataFrame
    3. Generates basic schema
    4. Updates state with results
    """

    def __init__(self, data_dir: str = "data"):
        self.csv_handler = CSVHandler(data_dir)

    def process_csv(self, file_path: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a CSV file and update state.

        Args:
            file_path: Path to the CSV file
            state: Current system state

        Returns:
            Updated state with CSV processing results
        """
        try:
            # Update state to processing
            state = update_state(state, status="processing")

            # Validate CSV file
            is_valid, error_msg = self.csv_handler.validate_csv_file(file_path)
            if not is_valid:
                raise ValueError(f"CSV validation failed: {error_msg}")

            # Generate dataset ID
            dataset_id = self.csv_handler.generate_dataset_id(file_path)

            # Process CSV file
            df, schema = self.csv_handler.process_csv(file_path)

            # Update state with results
            state = update_state(
                state,
                source_type="csv",
                dataset_id=dataset_id,
                df=df,  # Store DataFrame directly
                schema=schema,
                status="completed"
            )

            return state

        except Exception as e:
            # Update state with error
            error_msg = f"Ingestion failed: {str(e)}"
            state = update_state(state, error=error_msg, status="error")
            return state


# Simple function interface
def process_csv_file(file_path: str, state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simple function to process a CSV file.

    Args:
        file_path: Path to the CSV file
        state: Current system state

    Returns:
        Updated state with CSV processing results
    """
    agent = IngestionAgent()
    return agent.process_csv(file_path, state)
