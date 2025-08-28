import pandas as pd
import sqlite3
import uuid
from pathlib import Path


class SQLHandler:

    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    # =============================================
    # 1. VALIDATION METHODS (Check before you do)
    # =============================================

    def validate_sqlite_file(self, db_path):
        """Check if the SQLite database is valid before processing"""
        try:
            if not Path(db_path).exists():
                return False, "Database file does not exist"

            if not db_path.lower().endswith(('.db', '.sqlite', '.sqlite3')):
                return False, "File must be a SQLite database"

            file_size = Path(db_path).stat().st_size
            if file_size == 0:
                return False, "Database file is empty"

            # Test connection and check for tables
            conn = sqlite3.connect(db_path)
            tables_query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            tables_df = pd.read_sql_query(tables_query, conn)
            conn.close()

            if tables_df.empty:
                return False, "No tables found in database"

            return True, f"SQLite database has {len(tables_df)} tables"

        except Exception as e:
            return False, f"SQLite validation error: {str(e)}"

    # =============================================
    # 2. PROCESSING METHODS (The main work)
    # =============================================

    def process_sqlite_file(self, db_path):
        """Process SQLite file - find tables and read data"""
        try:
            conn = sqlite3.connect(db_path)

            # Step 1: Find all tables
            tables_query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            tables_df = pd.read_sql_query(tables_query, conn)

            if tables_df.empty:
                raise ValueError("No tables found in SQLite database")

            table_names = tables_df['name'].tolist()

            # Step 2: Limit to max 3 tables for simplicity
            if len(table_names) > 3:
                table_names = table_names[:3]
                print(
                    f"📋 Found {len(tables_df)} tables, using first 3: {table_names}")
            else:
                print(f"📋 Found {len(table_names)} tables: {table_names}")

            # Step 3: Read tables and combine simply
            all_dataframes = []

            for table_name in table_names:
                # Read max 1000 rows per table
                query = f"SELECT * FROM {table_name} LIMIT 1000"
                df = pd.read_sql_query(query, conn)

                # Add table name as prefix to columns
                df = df.add_prefix(f"{table_name}_")
                all_dataframes.append(df)

                print(
                    f"   📊 {table_name}: {len(df)} rows, {len(df.columns)} columns")

            # Step 4: Simple combination - put tables side by side
            if len(all_dataframes) == 1:
                combined_df = all_dataframes[0]
            else:
                combined_df = pd.concat(all_dataframes, axis=1, sort=False)

            schema = self._get_basic_schema(combined_df, table_names)
            conn.close()

            print(
                f"✅ Combined {len(table_names)} tables: {len(combined_df)} rows, {len(combined_df.columns)} columns")
            return combined_df, schema

        except Exception as e:
            raise ValueError(f"Failed to process SQLite file: {str(e)}")

    # =============================================
    # 3. UTILITY METHODS (Smaller helpers)
    # =============================================

    def generate_dataset_id(self, db_path):
        """Generate a unique ID for this dataset"""
        filename = Path(db_path).stem
        short_uuid = str(uuid.uuid4())[:8]
        return f"sqlite_{filename}_{short_uuid}"

    # =============================================
    # 4. HELPER METHODS (Supporting functions)
    # =============================================

    def _get_basic_schema(self, df, table_names):
        """Extract basic information about the combined data"""
        schema = {
            "columns": list(df.columns),
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "data_types": {},
            "tables_found": table_names,
            "note": f"Data from {len(table_names)} tables, max 1000 rows each"
        }

        for col in df.columns:
            schema["data_types"][col] = str(df[col].dtype)

        return schema
