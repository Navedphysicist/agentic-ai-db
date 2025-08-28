"""
Step 1: Ingestion Agent Demo
Educational demo showing how the first AI agent works.
Perfect for beginners learning AI agent concepts.
"""

from shared.state import create_initial_state, get_status_summary
from agents.ingestion import process_csv_file, ingest_data_file
import sys
from pathlib import Path
import pandas as pd
import os

sys.path.append(str(Path(__file__).parent))


def create_sample_csv():
    data = {
        'order_date': ['2024-01-15', '2024-01-20', '2024-02-01', '2024-02-15', '2024-03-01'],
        'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'],
        'category': ['Electronics', 'Accessories', 'Accessories', 'Electronics', 'Accessories'],
        'quantity': [2, 5, 3, 1, 4],
        'unit_price': [1200.00, 25.99, 89.99, 299.99, 79.99],
        'customer_region': ['North', 'South', 'East', 'West', 'North']
    }

    df = pd.DataFrame(data)
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    csv_path = data_dir / "sample_sales.csv"
    df.to_csv(csv_path, index=False)

    print(f"Created sample CSV file: {csv_path}")
    print(f"Sample data preview:")
    print(df.head())
    print(f"Data info: {len(df)} rows, {len(df.columns)} columns")

    return str(csv_path)


def upload_csv_file():
    print("\nUpload Your Own CSV File")
    print("=" * 40)

    file_path = input(
        "Enter the path to your CSV file (or press Enter to use sample): ").strip()

    if not file_path:
        print("Using sample CSV file...")
        return create_sample_csv()

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        print("Using sample CSV file instead...")
        return create_sample_csv()

    if not file_path.lower().endswith('.csv'):
        print(f"File is not a CSV: {file_path}")
        print("Using sample CSV file instead...")
        return create_sample_csv()

    print(f"Using your CSV file: {file_path}")
    return file_path


def display_ingestion_results(state):
    print(f"\nState after ingestion:")
    print(f"Source type: {state.get('source_type')}")
    print(f"Dataset ID: {state.get('dataset_id')}")
    print(f"Status: {state.get('status')}")

    if state.get('schema'):
        schema = state['schema']
        print(f"\nSchema:")
        print(f"Total rows: {schema.get('total_rows')}")
        print(f"Total columns: {schema.get('total_columns')}")
        print(f"Columns: {schema.get('columns')}")
        print(f"Data types: {schema.get('data_types')}")

    if state.get('df') is not None:
        df = state['df']
        print(f"\nDataFrame loaded:")
        print(f"Shape: {df.shape}")
        print(f"First few rows:")
        print(df.head())


def demo_ingestion_agent():
    print("🚀 Step 1: Ingestion Agent Demo")
    print("=" * 50)
    print("Learning how the first AI agent processes data")

    print("\n📋 1. Creating initial state...")
    state = create_initial_state()
    print(f"   Initial state: {get_status_summary(state)}")
    print("   💡 The state tracks what our agent is doing")

    print("\n📁 2. Getting CSV file...")
    csv_path = upload_csv_file()
    print("   💡 Agent will automatically read ALL the data")
    print("   💡 No queries needed - just upload and let the agent work!")

    print("\n⚙️ 3. Running the Ingestion Agent...")
    print("   Agent discovers and ingests everything automatically!")

    try:
        state = process_csv_file(csv_path, state)
        print(f"   Status: {get_status_summary(state)}")

        display_ingestion_results(state)

    except Exception as e:
        print(f"   ❌ Unexpected error: {str(e)}")

    print("\n📊 4. Understanding the Results...")
    print(f"   Final status: {get_status_summary(state)}")

    if state.get('error'):
        print(f"   ❌ What went wrong: {state['error']}")
        print("   💡 Error handling helps us understand problems")
    else:
        print(f"   ✅ Success! Data is now ready for analysis")
        print("   💡 The agent has completed its single responsibility")

    return state


if __name__ == "__main__":
    print("🎯 Agentic AI DB - Step 1: Ingestion Agent")
    print("=" * 60)
    print("📚 Learning AI Agents One Step at a Time")

    final_state = demo_ingestion_agent()

    print("\n" + "=" * 60)
    print("🎓 What We Learned About AI Agents")
    print("=" * 60)
    print("✅ State Management: How agents track their progress")
    print("✅ File Validation: Safe file handling practices")
    print("✅ Data Processing: Using pandas for CSV files")
    print("✅ Error Handling: Graceful failure management")
    print("✅ Agent Design: Single-responsibility principle")
    print("✅ Unique IDs: Generate identifiers for datasets")

    print("\n🔍 Key Concepts:")
    print("• An AI agent is a program that performs specific tasks")
    print("• State helps track what the agent is doing")
    print("• Validation prevents errors before processing")
    print("• Schemas describe the structure of data")

    print("\n🗃️ Data Sources Supported:")
    print("• CSV Files: What we just demonstrated")
    print("• SQLite Databases: Local database files")
    print("• SQL Databases: PostgreSQL, MySQL, etc.")
    print("• MongoDB: Document databases")
    print("• All with the SAME agent interface!")

    print("\n🚀 Next Steps:")
    print("• Master this Ingestion Agent first")
    print("• Try the multi-source demo: python demo_multi_source_ingestion.py")
    print("• Understand each part of the code")
    print("• Then we'll ask about building the next agent!")
    print("\n💡 One agent at a time = better learning!")
