"""
Simplified demo script for the Ingestion Agent.
Shows basic CSV processing and schema inference.
Includes upload functionality for testing with custom CSV files.
"""

from shared.state import create_initial_state, get_status_summary
from agents.ingestion import process_csv_file
import sys
from pathlib import Path
import pandas as pd
import os

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))


def create_sample_csv():
    """Create a sample CSV file for testing."""
    # Sample sales data
    data = {
        'order_date': ['2024-01-15', '2024-01-20', '2024-02-01', '2024-02-15', '2024-03-01'],
        'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'],
        'category': ['Electronics', 'Accessories', 'Accessories', 'Electronics', 'Accessories'],
        'quantity': [2, 5, 3, 1, 4],
        'unit_price': [1200.00, 25.99, 89.99, 299.99, 79.99],
        'customer_region': ['North', 'South', 'East', 'West', 'North']
    }

    df = pd.DataFrame(data)

    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Save sample CSV
    csv_path = data_dir / "sample_sales.csv"
    df.to_csv(csv_path, index=False)

    print(f"✅ Created sample CSV file: {csv_path}")
    print(f"📊 Sample data preview:")
    print(df.head())
    print(f"\n📋 Data info:")
    print(f"   - Rows: {len(df)}")
    print(f"   - Columns: {len(df.columns)}")

    return str(csv_path)


def upload_csv_file():
    """Allow user to upload their own CSV file."""
    print("\n📁 Upload Your Own CSV File")
    print("=" * 40)

    # Get file path from user
    file_path = input(
        "Enter the path to your CSV file (or press Enter to use sample): ").strip()

    if not file_path:
        print("   Using sample CSV file...")
        return create_sample_csv()

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"   ❌ File not found: {file_path}")
        print("   Using sample CSV file instead...")
        return create_sample_csv()

    # Check if it's a CSV file
    if not file_path.lower().endswith('.csv'):
        print(f"   ❌ File is not a CSV: {file_path}")
        print("   Using sample CSV file instead...")
        return create_sample_csv()

    print(f"   ✅ Using your CSV file: {file_path}")
    return file_path


def demo_ingestion_agent():
    """Demonstrate the Ingestion Agent in action."""
    print("🚀 Starting Simplified Ingestion Agent Demo")
    print("=" * 50)

    # Step 1: Create initial state
    print("\n1️⃣ Creating initial state...")
    state = create_initial_state()
    print(f"   Initial state: {get_status_summary(state)}")

    # Step 2: Get CSV file (sample or user upload)
    print("\n2️⃣ Getting CSV file...")
    csv_path = upload_csv_file()

    # Step 3: Process CSV with Ingestion Agent
    print("\n3️⃣ Processing CSV with Ingestion Agent...")
    try:
        state = process_csv_file(csv_path, state)
        print(f"   ✅ CSV processed successfully!")
        print(f"   Status: {get_status_summary(state)}")

        # Show what was added to state
        print(f"\n📊 State after ingestion:")
        print(f"   - Source type: {state.get('source_type')}")
        print(f"   - Dataset ID: {state.get('dataset_id')}")
        print(f"   - Status: {state.get('status')}")

        # Show schema
        if state.get('schema'):
            schema = state['schema']
            print(f"\n🔍 Schema:")
            print(f"   - Total rows: {schema.get('total_rows')}")
            print(f"   - Total columns: {schema.get('total_columns')}")
            print(f"   - Columns: {schema.get('columns')}")
            print(f"   - Data types: {schema.get('data_types')}")

        # Show DataFrame info
        if state.get('df') is not None:
            df = state['df']
            print(f"\n📊 DataFrame loaded:")
            print(f"   - Shape: {df.shape}")
            print(f"   - First few rows:")
            print(df.head())

    except Exception as e:
        print(f"   ❌ Error processing CSV: {str(e)}")

    # Step 4: Show final state
    print("\n4️⃣ Final state summary...")
    print(f"   Final status: {get_status_summary(state)}")

    if state.get('error'):
        print(f"   ❌ Errors encountered: {state['error']}")
    else:
        print(f"   ✅ Ingestion completed successfully!")
        print(f"   🎯 Ready for next agent (Planner)")

    return state


if __name__ == "__main__":
    print("🎯 Agentic AI DB - Simplified Ingestion Agent Demo")
    print("=" * 60)

    # Run main demo
    final_state = demo_ingestion_agent()

    print("\n" + "=" * 60)
    print("🎉 Demo completed!")
    print("\n📚 What we learned:")
    print("   ✅ Ingestion Agent can process CSV files")
    print("   ✅ Basic schema inference works")
    print("   ✅ DataFrame is stored in state")
    print("   ✅ Simple state management")
    print("   ✅ Upload functionality works")
    print("\n🚀 Next step: Build the Planner agent!")
