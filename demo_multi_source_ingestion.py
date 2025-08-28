"""
Multi-Source Ingestion Agent Demo
Shows how the Ingestion Agent automatically discovers and ingests data from different sources.
Perfect for learning how one agent can handle different data types WITHOUT requiring user queries.
"""

from shared.state import create_initial_state, get_status_summary
from agents.ingestion import process_csv_file, process_sqlite_file, process_json_file, ingest_data_file
from create_sample_databases import create_sample_sqlite, create_sample_json
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
    return str(csv_path)


def demo_csv_ingestion():
    print("\n" + "="*50)
    print("📊 CSV DATA SOURCE")
    print("="*50)
    print("🎯 User just uploads a CSV file - no queries needed!")

    state = create_initial_state()
    csv_path = create_sample_csv()

    print(f"📁 Processing CSV file: {csv_path}")
    print("   💡 Agent automatically reads ALL the data")

    state = process_csv_file(csv_path, state)

    if state.get('error'):
        print(f"❌ Error: {state['error']}")
    else:
        print(f"✅ Status: {get_status_summary(state)}")

    return state


def demo_sqlite_ingestion():
    print("\n" + "="*50)
    print("🗄️ SQLITE DATA SOURCE")
    print("="*50)
    print("🎯 User just uploads a SQLite file - agent discovers ALL tables!")

    state = create_initial_state()
    db_path = create_sample_sqlite()

    print(f"📁 Processing SQLite database: {db_path}")
    print("   💡 Agent automatically discovers and reads ALL tables")
    print("   💡 No SQL queries needed from the user!")

    state = process_sqlite_file(db_path, state)

    if state.get('error'):
        print(f"❌ Error: {state['error']}")
    else:
        print(f"✅ Status: {get_status_summary(state)}")

    return state


def demo_json_ingestion():
    print("\n" + "="*50)
    print("📄 JSON DATA SOURCE")
    print("="*50)
    print("🎯 User just uploads a JSON file - agent reads ALL the data!")

    state = create_initial_state()
    json_path = create_sample_json()

    print(f"📁 Processing JSON file: {json_path}")
    print("   💡 Agent automatically reads ALL documents")
    print("   💡 Perfect for MongoDB-style data!")

    state = process_json_file(json_path, state)

    if state.get('error'):
        print(f"❌ Error: {state['error']}")
    else:
        print(f"✅ Status: {get_status_summary(state)}")

    return state


def demo_universal_ingestion():
    print("\n" + "="*50)
    print("🔄 UNIVERSAL FILE INGESTION")
    print("="*50)
    print("🎯 Just give the agent ANY file - it figures out the rest!")

    # Test 1: Auto-ingest CSV
    print("\n🔍 Test 1: Auto-ingesting CSV file")
    state1 = create_initial_state()
    csv_path = "data/sample_sales.csv"
    state1 = ingest_data_file(csv_path, state1)
    print(f"   Result: {get_status_summary(state1)}")

    # Test 2: Auto-ingest SQLite
    print("\n🔍 Test 2: Auto-ingesting SQLite database")
    state2 = create_initial_state()
    db_path = "data/sample_inventory.db"
    state2 = ingest_data_file(db_path, state2)
    print(f"   Result: {get_status_summary(state2)}")

    # Test 3: Auto-ingest JSON
    print("\n🔍 Test 3: Auto-ingesting JSON file")
    state3 = create_initial_state()
    json_path = "data/sample_customers.json"
    state3 = ingest_data_file(json_path, state3)
    print(f"   Result: {get_status_summary(state3)}")

    return state1, state2, state3


def display_results(state, data_source_name):
    print(f"\n📋 {data_source_name} Results:")
    print(f"   Source type: {state.get('source_type')}")
    print(f"   Dataset ID: {state.get('dataset_id')}")
    print(f"   Status: {state.get('status')}")

    if state.get('schema'):
        schema = state['schema']
        print(
            f"   Data: {schema.get('total_rows')} rows, {schema.get('total_columns')} columns")
        print(f"   Columns: {schema.get('columns')[:5]}...")  # First 5 columns

        # Show discovered tables/collections if any
        if 'tables_discovered' in schema:
            print(f"   Tables discovered: {schema['tables_discovered']}")
        if 'collections_discovered' in schema:
            print(
                f"   Collections discovered: {schema['collections_discovered']}")

    if state.get('df') is not None:
        df = state['df']
        print(f"   Sample data (first 2 rows):")
        print(df.head(2).to_string(index=False))


def demo_multi_source_ingestion():
    print("🚀 Multi-Source Ingestion Agent Demo")
    print("=" * 60)
    print("🎯 Learning: UPLOAD ONLY - Agent discovers and ingests ALL data automatically!")

    print("\n💡 Key Concept: The Ingestion Agent works like this:")
    print("   1. User uploads ANY data file (CSV, SQLite, JSON, etc.)")
    print("   2. Agent auto-detects the file type")
    print("   3. Agent discovers ALL tables/collections in the file")
    print("   4. Agent reads ALL the data automatically")
    print("   5. User can then ask natural language questions later!")
    print("   ✅ NO SQL queries needed from the user!")

    # Demo 1: CSV Ingestion
    csv_state = demo_csv_ingestion()

    # Demo 2: SQLite Ingestion
    sqlite_state = demo_sqlite_ingestion()

    # Demo 3: JSON Ingestion
    json_state = demo_json_ingestion()

    # Demo 4: Universal Ingestion
    auto_states = demo_universal_ingestion()

    # Show results
    print("\n" + "="*60)
    print("📊 COMPARISON OF AUTOMATIC INGESTION RESULTS")
    print("="*60)

    if not csv_state.get('error'):
        display_results(csv_state, "CSV")

    if not sqlite_state.get('error'):
        display_results(sqlite_state, "SQLITE")

    if not json_state.get('error'):
        display_results(json_state, "JSON")

    return csv_state, sqlite_state, json_state


if __name__ == "__main__":
    print("🎯 Agentic AI DB - Automatic Multi-Source Ingestion")
    print("=" * 70)
    print("📚 Learning: Upload Files → Agent Discovers Everything → Ask Questions Later")

    csv_state, sqlite_state, json_state = demo_multi_source_ingestion()

    print("\n" + "=" * 70)
    print("🎓 What We Learned About Automatic Ingestion")
    print("=" * 70)
    print("✅ Upload Only: Users just upload files, no technical queries needed")
    print("✅ Auto-Discovery: Agent automatically finds all tables/collections")
    print("✅ Complete Ingestion: Agent reads ALL available data")
    print("✅ Smart Detection: Agent knows how to handle each file type")
    print("✅ Unified Storage: All data ends up in the same format (DataFrame)")
    print("✅ Ready for Questions: Data is now ready for natural language queries")

    print("\n🔍 Real-World Workflow:")
    print("1. 📁 User uploads: sales.csv, inventory.db, customers.json")
    print("2. 🤖 Agent automatically ingests ALL data from ALL files")
    print("3. 💬 User asks: 'What are the top selling products by region?'")
    print("4. 🧠 Planner Agent creates execution plan")
    print("5. ⚙️ Executor Agent runs the analysis")
    print("6. 📝 Summarizer Agent explains the results")

    print("\n🗃️ File Types Supported:")
    print("• CSV Files: Automatic column detection and data type inference")
    print("• SQLite: Discovers all tables and reads everything")
    print("• JSON Files: Reads documents for MongoDB-style data")
    print("• SQL Databases: Discovers and reads all accessible tables")
    print("• MongoDB: Discovers and reads all collections")

    print("\n🚀 Next Steps:")
    print("• Try uploading your own data files")
    print("• See how the agent handles different file types")
    print("• Understand the 'upload and forget' philosophy")
    print("• Ready to build the Planner Agent for natural language queries!")
    print("\n💡 This is how real data platforms work - automatic ingestion!")
