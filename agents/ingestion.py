from data.csv_handler import CSVHandler
from data.sql_handler import SQLHandler
from data.mongo_handler import MongoHandler
from shared.state import update_state


# =============================================
# 1. VALIDATION & DETECTION (Check what we have)
# =============================================

def detect_data_source(file_path):
    """Auto-detect data source type based on file extension"""
    if isinstance(file_path, str):
        if file_path.lower().endswith('.csv'):
            return "csv"
        elif file_path.lower().endswith(('.db', '.sqlite', '.sqlite3')):
            return "sqlite"
        elif file_path.lower().endswith(('.json', '.jsonl')):
            return "json"

    return "unknown"


# =============================================
# 2. PROCESSING METHODS (The main work)
# =============================================

def process_csv_file(file_path, state):
    """Process CSV file using CSV handler"""
    state = update_state(state, status="processing")

    csv_handler = CSVHandler()

    # Step 1: Validate first
    is_valid, message = csv_handler.validate_csv_file(file_path)
    if not is_valid:
        state = update_state(
            state, error=f"CSV validation failed: {message}", status="error")
        return state

    # Step 2: Process the file
    try:
        df, schema = csv_handler.process_csv(file_path)
        dataset_id = csv_handler.generate_dataset_id(file_path)

        state = update_state(
            state,
            source_type="csv",
            dataset_id=dataset_id,
            df=df,
            schema=schema,
            status="completed"
        )

        print(f"✅ CSV processed successfully!")
        print(f"📊 Dataset ID: {dataset_id}")
        print(f"📊 Loaded {len(df)} rows and {len(df.columns)} columns")

        return state

    except Exception as e:
        state = update_state(
            state, error=f"CSV processing failed: {str(e)}", status="error")
        return state


def process_sqlite_file(db_path, state):
    """Process SQLite database file - automatically discovers tables (max 3 tables, 1000 rows each)"""
    state = update_state(state, status="processing")

    sql_handler = SQLHandler()

    # Step 1: Validate first
    is_valid, message = sql_handler.validate_sqlite_file(db_path)
    if not is_valid:
        state = update_state(
            state, error=f"SQLite validation failed: {message}", status="error")
        return state

    # Step 2: Process the database
    try:
        df, schema = sql_handler.process_sqlite_file(db_path)
        dataset_id = sql_handler.generate_dataset_id(db_path)

        state = update_state(
            state,
            source_type="sqlite",
            dataset_id=dataset_id,
            df=df,
            schema=schema,
            status="completed"
        )

        print(f"✅ SQLite database processed successfully!")
        print(f"📊 Dataset ID: {dataset_id}")
        print(f"📊 Found {len(schema.get('tables_found', []))} tables")

        return state

    except Exception as e:
        state = update_state(
            state, error=f"SQLite processing failed: {str(e)}", status="error")
        return state


def process_json_file(file_path, state):
    """Process JSON file as document data (max 1000 documents)"""
    state = update_state(state, status="processing")

    mongo_handler = MongoHandler()

    # Step 1: Validate first
    is_valid, message = mongo_handler.validate_json_file(file_path)
    if not is_valid:
        state = update_state(
            state, error=f"JSON validation failed: {message}", status="error")
        return state

    # Step 2: Process the file
    try:
        df, schema = mongo_handler.process_json_file(file_path)
        dataset_id = mongo_handler.generate_dataset_id(file_path)

        state = update_state(
            state,
            source_type="json",
            dataset_id=dataset_id,
            df=df,
            schema=schema,
            status="completed"
        )

        print(f"✅ JSON file processed successfully!")
        print(f"📊 Dataset ID: {dataset_id}")
        print(f"📊 Loaded {len(df)} documents and {len(df.columns)} fields")

        return state

    except Exception as e:
        state = update_state(
            state, error=f"JSON processing failed: {str(e)}", status="error")
        return state


# =============================================
# 3. MAIN INGESTION FUNCTION (The entry point)
# =============================================

def ingest_data_file(file_path, state):
    """
    Simple function for file-based ingestion.
    Just provide a file path - the agent figures out the rest!

    Limits for students:
    - CSV: Max 10,000 rows
    - SQLite: Max 3 tables, 1000 rows each
    - JSON: Max 1000 documents
    """
    print(f"🔍 Auto-detecting data source: {file_path}")

    # Step 1: Detect what type of file this is
    source_type = detect_data_source(file_path)
    print(f"📋 Detected source type: {source_type}")

    # Step 2: Route to the correct processor
    if source_type == "csv":
        return process_csv_file(file_path, state)
    elif source_type == "sqlite":
        return process_sqlite_file(file_path, state)
    elif source_type == "json":
        return process_json_file(file_path, state)
    else:
        state = update_state(
            state, error=f"Unsupported file type: {file_path}", status="error")
        return state
