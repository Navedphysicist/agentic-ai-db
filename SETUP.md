# Setup Guide - Agentic AI DB

This guide helps you set up the project correctly with a virtual environment.

## Prerequisites

- Python 3.8 or higher
- pip (usually comes with Python)

## Step-by-Step Setup

### 1. Clone or Download the Project
```bash
# If you have the project folder, navigate to it
cd agentic-ai-db
```

### 2. Create Virtual Environment
```bash
# Create a new virtual environment
python3 -m venv venv

# You should see a 'venv' folder created
```

### 3. Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

**You'll know it's activated when you see `(venv)` in your terminal prompt**

### 4. Install Requirements
```bash
# Make sure you're in the project directory with requirements.txt
pip install -r requirements.txt
```

### 5. Verify Installation
```bash
# Test that everything works
python test_ingestion_agent.py
```

You should see:
```
🎉 All tests passed! Ingestion Agent is working perfectly!
```

### 6. Try the Demos

**Basic CSV Demo:**
```bash
python demo_ingestion.py
```

**Multi-Source Demo:**
```bash
python demo_multi_source_ingestion.py
```

**Create Sample Data:**
```bash
python create_sample_databases.py
```

## Deactivating Virtual Environment

When you're done working:
```bash
deactivate
```

## Troubleshooting

### Common Issues:

**1. `python3` command not found:**
- Try `python` instead of `python3`
- Make sure Python is installed

**2. Permission errors:**
- Make sure you have write permissions in the directory
- Try running terminal as administrator (Windows)

**3. Package installation fails:**
- Make sure virtual environment is activated
- Try upgrading pip: `pip install --upgrade pip`

**4. Import errors:**
- Make sure virtual environment is activated
- Make sure you're in the correct directory

### Checking Your Setup:

```bash
# Check Python version
python --version

# Check if virtual environment is active
which python  # Should show path with 'venv'

# Check installed packages
pip list
```

## For Students

**Remember:**
1. **Always activate** the virtual environment before working
2. **Install packages only** when virtual environment is active
3. **Deactivate** when you're done
4. **Don't commit** the `venv` folder to git

## For Teachers

This setup ensures:
- ✅ Isolated environment per student
- ✅ No conflicts with system Python
- ✅ Reproducible setup across machines
- ✅ Safe package installation

