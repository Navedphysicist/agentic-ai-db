# Agentic AI DB - Step 1: Multi-Source Ingestion Agent

A powerful, beginner-friendly project to learn AI agents by building them step-by-step.

**Current Focus: Multi-Source Ingestion Agent**

## What the Ingestion Agent Does

The Ingestion Agent is smart enough to handle multiple data sources with a single, consistent interface:

### ✅ Supported Data Sources
- **CSV Files**: `.csv` files with pandas processing
- **SQLite Databases**: `.db/.sqlite` files with SQL queries
- **SQL Databases**: PostgreSQL, MySQL with connection strings
- **MongoDB**: Document collections with query support

### 🔍 Key Features
- **Auto-Detection**: Automatically detects data source types
- **Consistent Interface**: Same functions work for all sources
- **Specialized Handlers**: Optimized processing for each data type
- **Unified Output**: All sources produce the same state format
- **Error Handling**: Graceful failures for all source types
- **Validation**: Each source validates before processing

## Quick Start

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Basic CSV demo:
```bash
python demo_ingestion.py
```

4. Multi-source demo:
```bash
python demo_multi_source_ingestion.py
```

5. Create sample databases:
```bash
python create_sample_databases.py
```

6. Run comprehensive tests:
```bash
python test_ingestion_agent.py
```

## Project Structure

```
agentic-ai-db/
├── agents/
│   └── ingestion.py           # Multi-source Ingestion Agent
├── data/
│   ├── csv_handler.py         # CSV processing
│   ├── sql_handler.py         # SQL/SQLite processing  
│   ├── mongo_handler.py       # MongoDB processing
│   └── sample_*.csv/db        # Sample data files
├── shared/
│   └── state.py               # State management
├── config/
│   └── gemini_config.py       # AI model configuration
├── demo_ingestion.py          # Basic CSV demo
├── demo_multi_source_ingestion.py  # Multi-source demo
└── create_sample_databases.py # Create sample data
```

## What Students Learn

### 🎓 Core Concepts
1. **Agent Pattern**: One interface, multiple implementations
2. **Handler Pattern**: Specialized classes for each data type
3. **State Management**: Consistent state across all sources
4. **Auto-Detection**: Smart routing based on data source type
5. **Error Handling**: Graceful failure management
6. **Data Validation**: Safe processing practices

### 🗃️ Real-World Skills
- Working with multiple data formats
- Database connectivity and querying
- Data pipeline design
- Error handling strategies
- Clean architecture patterns

## Sample Usage

### CSV Processing
```python
from agents.ingestion import process_csv_file
from shared.state import create_initial_state

state = create_initial_state()
state = process_csv_file("data/sample_sales.csv", state)
```

### SQLite Processing
```python
from agents.ingestion import process_sqlite_file

state = create_initial_state()
state = process_sqlite_file("data/sample_inventory.db", "SELECT * FROM products", state)
```

### Auto-Detection
```python
from agents.ingestion import process_data_source

# Auto-detects CSV
state = process_data_source("data/sample_sales.csv", state)

# Auto-detects SQLite
state = process_data_source("data/sample_inventory.db", state, query="SELECT * FROM products")
```

## Sample Output

```
🚀 Multi-Source Ingestion Agent Demo

📊 CSV DATA SOURCE
✅ CSV processed successfully!
📊 Dataset ID: csv_sample_sales_a1b2c3d4
📊 Loaded 5 rows and 6 columns

🗄️ SQLITE DATA SOURCE  
✅ SQLite database processed successfully!
📊 Dataset ID: sql_sample_inventory_x7y8z9w0
📊 Loaded 5 rows and 6 columns

🔄 UNIVERSAL DATA PROCESSOR
Auto-detects and processes different data sources!
```

## Learning Philosophy

**One agent at a time, master each step before moving forward!**

- Start with understanding how the agent works with CSV files
- Learn how the same agent handles databases
- Understand the architecture patterns
- Master multi-source concepts
- Then move to the next agent

## Next Steps

After mastering the Multi-Source Ingestion Agent, we'll add:
- **Planner Agent**: Converts questions to execution plans
- **Executor Agent**: Executes data operations  
- **Summarizer Agent**: Creates human-readable summaries

**Ready when you are!** This agent foundation prepares you for the complete 4-agent system.