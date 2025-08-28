"""
Simplified CSV data handler for the Ingestion Agent.
Core functionality only - read CSV, basic schema, store DataFrame.
"""

import pandas as pd
from typing import Dict, Any, Tuple
from pathlib import Path


class CSVHandler:
    """Simple CSV file processing and basic schema inference."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def process_csv(self, file_path: str, max_rows: int = 10000) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Process a CSV file and return DataFrame + basic schema.

        Args:
            file_path: Path to the CSV file
            max_rows: Maximum rows to read (will be applied after reading)

        Returns:
            Tuple of (DataFrame, basic_schema)
        """
        try:
            # Read CSV with pyarrow (without nrows parameter)
            df = pd.read_csv(
                file_path,
                engine='pyarrow',
                parse_dates=True
            )

            # Apply row limit after reading (pyarrow compatible)
            if len(df) > max_rows:
                df = df.head(max_rows)

            # Generate basic schema
            schema = self._get_basic_schema(df)

            return df, schema

        except Exception as e:
            raise ValueError(f"Failed to process CSV file: {str(e)}")

    def _get_basic_schema(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get basic schema information from DataFrame."""
        schema = {
            "columns": list(df.columns),
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "data_types": {}
        }

        # Add data types for each column
        for col in df.columns:
            schema["data_types"][col] = str(df[col].dtype)

        return schema

    def validate_csv_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Basic CSV file validation.

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Check file exists
            if not Path(file_path).exists():
                return False, "File does not exist"

            # Check file extension
            if not file_path.lower().endswith('.csv'):
                return False, "File must be a CSV"

            return True, "File is valid"

        except Exception as e:
            return False, f"Validation error: {str(e)}"

    def generate_dataset_id(self, file_path: str) -> str:
        """Generate a simple dataset ID."""
        # Simple ID based on filename
        filename = Path(file_path).stem
        return f"csv_{filename}_{len(filename)}"
