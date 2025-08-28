import pandas as pd
import uuid
from pathlib import Path


class MongoHandler:

    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    # =============================================
    # 1. VALIDATION METHODS (Check before you do)
    # =============================================

    def validate_json_file(self, file_path):
        """Check if the JSON file is valid before processing"""
        try:
            if not Path(file_path).exists():
                return False, "JSON file does not exist"

            if not file_path.lower().endswith(('.json', '.jsonl')):
                return False, "File must be a JSON file"

            file_size = Path(file_path).stat().st_size
            if file_size == 0:
                return False, "JSON file is empty"

            # Test JSON parsing
            import json
            with open(file_path, 'r') as f:
                data = json.load(f)

            if isinstance(data, (dict, list)):
                item_count = len(data) if isinstance(data, list) else 1
                return True, f"Valid JSON file with {item_count} items"
            else:
                return False, "JSON file must contain an object or array"

        except Exception as e:
            return False, f"JSON validation error: {str(e)}"

    # =============================================
    # 2. PROCESSING METHODS (The main work)
    # =============================================

    def process_json_file(self, file_path):
        """Process JSON file and convert to DataFrame"""
        try:
            import json

            # Step 1: Read JSON file
            with open(file_path, 'r') as f:
                data = json.load(f)

            # Step 2: Make sure data is a list of documents
            if isinstance(data, dict):
                data = [data]
            elif not isinstance(data, list):
                raise ValueError("JSON file must contain an object or array")

            # Step 3: Limit to max 1000 documents for simplicity
            if len(data) > 1000:
                data = data[:1000]
                print(f"📋 Large JSON file detected, using first 1000 documents")

            print(f"📋 Processing {len(data)} documents from JSON file")

            # Step 4: Convert to DataFrame
            df = pd.DataFrame(data)

            # Step 5: Convert complex nested objects to strings for simplicity
            for col in df.columns:
                if df[col].dtype == 'object':
                    # Check if column contains dictionaries or lists
                    sample_value = df[col].dropna(
                    ).iloc[0] if not df[col].dropna().empty else None
                    if isinstance(sample_value, (dict, list)):
                        df[col] = df[col].astype(str)

            schema = self._get_basic_schema(df, file_path)

            print(
                f"✅ JSON processed: {len(df)} documents, {len(df.columns)} fields")
            return df, schema

        except Exception as e:
            raise ValueError(f"Failed to process JSON file: {str(e)}")

    # =============================================
    # 3. UTILITY METHODS (Smaller helpers)
    # =============================================

    def generate_dataset_id(self, file_path):
        """Generate a unique ID for this dataset"""
        filename = Path(file_path).stem
        short_uuid = str(uuid.uuid4())[:8]
        return f"json_{filename}_{short_uuid}"

    # =============================================
    # 4. HELPER METHODS (Supporting functions)
    # =============================================

    def _get_basic_schema(self, df, file_path):
        """Extract basic information about the JSON data"""
        schema = {
            "columns": list(df.columns),
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "data_types": {},
            "source_file": Path(file_path).name,
            "note": "JSON data processed as documents, max 1000 rows"
        }

        for col in df.columns:
            schema["data_types"][col] = str(df[col].dtype)

        return schema
