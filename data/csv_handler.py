import pandas as pd
import uuid
from pathlib import Path


class CSVHandler:

    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    # =============================================
    # 1. VALIDATION METHODS (Check before you do)
    # =============================================

    def validate_csv_file(self, file_path):
        """Check if the CSV file is valid before processing"""
        try:
            if not Path(file_path).exists():
                return False, "File does not exist"

            if not file_path.lower().endswith('.csv'):
                return False, "File must be a CSV"

            file_size = Path(file_path).stat().st_size
            if file_size == 0:
                return False, "File is empty"

            if file_size > 100 * 1024 * 1024:  # 100MB limit
                return False, "File too large (max 100MB)"

            return True, "File is valid"

        except Exception as e:
            return False, f"Validation error: {str(e)}"

    # =============================================
    # 2. PROCESSING METHODS (The main work)
    # =============================================

    def process_csv(self, file_path, max_rows=10000):
        """Process the CSV file and return data + schema"""
        try:
            df = pd.read_csv(
                file_path,
                engine='pyarrow',
                parse_dates=True
            )

            if len(df) > max_rows:
                print(f"Large dataset detected. Using first {max_rows} rows.")
                df = df.head(max_rows)

            schema = self._get_basic_schema(df)
            return df, schema

        except Exception as e:
            raise ValueError(f"Failed to process CSV file: {str(e)}")

    # =============================================
    # 3. UTILITY METHODS (Smaller helpers)
    # =============================================

    def generate_dataset_id(self, file_path):
        """Generate a unique ID for this dataset"""
        filename = Path(file_path).stem
        short_uuid = str(uuid.uuid4())[:8]
        return f"csv_{filename}_{short_uuid}"

    # =============================================
    # 4. HELPER METHODS (Supporting functions)
    # =============================================

    def _get_basic_schema(self, df):
        """Extract basic information about the data structure"""
        schema = {
            "columns": list(df.columns),
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "data_types": {}
        }

        for col in df.columns:
            schema["data_types"][col] = str(df[col].dtype)

        return schema
