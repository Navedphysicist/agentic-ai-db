# Agentic AI DB / Inventory System - Simplified

A conversational AI platform that lets users ask business questions in plain English and get instant answers from their data (CSV, SQL, MongoDB, Excel, Google Sheets).

## 🚀 Current Status: Phase 1 - Simplified Ingestion Agent Complete

We've successfully built a **simplified Ingestion Agent** - the first agent in our streamlined pipeline! 

### ✅ What's Working (Simplified)

- **Ingestion Agent**: Processes CSV files, basic schema inference
- **CSV Handler**: Simple CSV processing with pandas
- **State Management**: Minimal state with essential fields only
- **Basic Schema**: Column names and data types only
- **DataFrame Storage**: Direct DataFrame reference (no complex storage)

### 🏗️ Simplified Architecture

```
User Upload CSV → Ingestion Agent → CSV Handler → Basic Schema → DataFrame in State
                                    ↓
                              State Updated with:
                              - dataset_id
                              - schema (basic)  
                              - df (DataFrame)
                              - source_type
```

## 🎯 Simplified Approach: 4 Core Agents Only

We've streamlined the system to focus on **essential functionality only**:

1. **✅ Ingestion Agent** - CSV processing (working)
2. **🎯 Planner Agent** - Convert English to query plans (next)
3. **📋 Executor Agent** - Run approved plans
4. **📝 Summarizer Agent** - Generate explanations

**Removed for simplicity:**
- ~~Query Router~~ - Direct routing in Planner
- ~~Plan Guard~~ - Basic validation in Planner
- ~~Visualization Agent~~ - Tables only
- ~~Responder~~ - Frontend handles this
- ~~Complex state management~~ - Essential fields only

## 🎯 How to Use the Simplified Ingestion Agent

### 1. Basic Usage

```python
from shared.state import create_initial_state
from agents.ingestion import process_csv_file

# Create initial state
state = create_initial_state()

# Process a CSV file
state = process_csv_file("path/to/your/file.csv", state)

# Check results
print(f"Dataset ID: {state['dataset_id']}")
print(f"Schema: {state['schema']}")
print(f"DataFrame shape: {state['df'].shape}")
```

### 2. Run the Demo

```bash
cd agentic-ai-db
python demo_ingestion.py
```

This will:
- Create a sample CSV file
- Process it with the Ingestion Agent
- Show basic schema results
- Display the DataFrame

## 📊 What the Simplified Ingestion Agent Does

### For CSV Files:
1. **Validates** file (exists, CSV extension)
2. **Processes** with pandas + pyarrow
3. **Generates Basic Schema**:
   - Column names
   - Data types
   - Row/column counts
4. **Stores DataFrame** directly in state
5. **Updates State** with essential information

### Schema Output (Simplified):
```json
{
  "columns": ["order_date", "product", "category", "quantity", "unit_price"],
  "total_rows": 5,
  "total_columns": 5,
  "data_types": {
    "order_date": "object",
    "product": "object",
    "quantity": "int64",
    "unit_price": "float64"
  }
}
```

## 🔧 Technical Details (Simplified)

### Dependencies (Minimal)
- **pandas**: Data processing
- **pyarrow**: Fast CSV reading
- **langchain**: Basic AI framework

### File Structure (Streamlined)
```
agentic-ai-db/
├── agents/
│   └── ingestion.py          # Simple Ingestion Agent
├── data/
│   └── csv_handler.py        # Basic CSV processing
├── shared/
│   └── state.py              # Minimal state management
├── demo_ingestion.py         # Simple demo
└── requirements.txt           # Minimal dependencies
```

### State Management (Essential Only)
The state is a simple dictionary with only essential fields:
```python
{
    "session_id": "uuid",
    "source_type": "csv",
    "dataset_id": "csv_sample_sales_15",
    "df": <DataFrame>,  # Direct reference
    "schema": {...},     # Basic schema
    "status": "completed"
}
```

## 🚀 Next Steps

### Phase 1: Core Agents (Current)
- [x] **Ingestion Agent**: CSV processing working
- [ ] **Planner Agent**: Convert English to query plans
- [ ] **Executor Agent**: Execute approved plans
- [ ] **Summarizer Agent**: Generate explanations

### Phase 2: Simple Backend
- [ ] Basic FastAPI endpoints
- [ ] File upload handling
- [ ] Agent coordination

### Phase 3: Simple Frontend
- [ ] Basic HTML interface
- [ ] File upload + query input
- [ ] Results display

## 🎓 Educational Value (Simplified)

This simplified project demonstrates:
- **AI Agent Basics**: How agents work together
- **Natural Language Processing**: Converting questions to data operations
- **Data Processing**: Safe pandas operations
- **Simple Architecture**: Clean, understandable code
- **Minimal Complexity**: Focus on core functionality

## 🔒 Safety Features (Simplified)

- **Basic Validation**: File existence, CSV format
- **Safe Operations**: Read-only data processing
- **Simple Limits**: Basic row limits only

## 📝 Why Simplified?

- **Student-Friendly**: Easy to understand and extend
- **Focused Learning**: Core AI concepts without complexity
- **Quick Development**: Build working system faster
- **Maintainable**: Less code, fewer bugs
- **Extensible**: Easy to add features later

---

**Ready for the next agent?** The simplified Ingestion Agent has prepared the data. Now we need the **Planner Agent** to convert English questions into query plans!
