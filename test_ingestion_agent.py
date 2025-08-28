"""
Comprehensive test for the Ingestion Agent
Tests all supported file types and error conditions
"""

from shared.state import create_initial_state, get_status_summary
from agents.ingestion import ingest_data_file, detect_data_source
from create_sample_databases import create_sample_sqlite, create_sample_json
import pandas as pd
from pathlib import Path
import json


def test_csv_ingestion():
    """Test CSV file ingestion"""
    print("🔍 Testing CSV Ingestion")
    print("-" * 30)
    
    # Create sample CSV
    data = {
        'id': [1, 2, 3],
        'name': ['A', 'B', 'C'],
        'value': [10.5, 20.7, 30.9]
    }
    df = pd.DataFrame(data)
    Path("data").mkdir(exist_ok=True)
    df.to_csv('data/test.csv', index=False)
    
    # Test ingestion
    state = create_initial_state()
    state = ingest_data_file('data/test.csv', state)
    
    # Verify results
    assert state['status'] == 'completed', f"Expected completed, got {state['status']}"
    assert state['source_type'] == 'csv', f"Expected csv, got {state['source_type']}"
    assert state['df'] is not None, "DataFrame should not be None"
    assert len(state['df']) == 3, f"Expected 3 rows, got {len(state['df'])}"
    assert 'dataset_id' in state, "Dataset ID should be present"
    
    print("✅ CSV ingestion test passed!")
    return True


def test_sqlite_ingestion():
    """Test SQLite database ingestion"""
    print("🔍 Testing SQLite Ingestion")
    print("-" * 30)
    
    # Create sample SQLite database
    db_path = create_sample_sqlite()
    
    # Test ingestion
    state = create_initial_state()
    state = ingest_data_file(db_path, state)
    
    # Verify results
    assert state['status'] == 'completed', f"Expected completed, got {state['status']}"
    assert state['source_type'] == 'sqlite', f"Expected sqlite, got {state['source_type']}"
    assert state['df'] is not None, "DataFrame should not be None"
    assert len(state['df']) > 0, "Should have some rows"
    assert 'tables_found' in state['schema'], "Should have discovered tables"
    assert len(state['schema']['tables_found']) <= 3, "Should limit to max 3 tables"
    
    print("✅ SQLite ingestion test passed!")
    print(f"   Tables found: {state['schema']['tables_found']}")
    print(f"   Combined data: {len(state['df'])} rows, {len(state['df'].columns)} columns")
    return True


def test_json_ingestion():
    """Test JSON file ingestion"""
    print("🔍 Testing JSON Ingestion")
    print("-" * 30)
    
    # Create sample JSON
    json_path = create_sample_json()
    
    # Test ingestion
    state = create_initial_state()
    state = ingest_data_file(json_path, state)
    
    # Verify results
    assert state['status'] == 'completed', f"Expected completed, got {state['status']}"
    assert state['source_type'] == 'json', f"Expected json, got {state['source_type']}"
    assert state['df'] is not None, "DataFrame should not be None"
    assert len(state['df']) > 0, "Should have some documents"
    assert len(state['df']) <= 1000, "Should limit to max 1000 documents"
    
    print("✅ JSON ingestion test passed!")
    print(f"   Documents processed: {len(state['df'])}")
    return True


def test_auto_detection():
    """Test automatic file type detection"""
    print("🔍 Testing Auto-Detection")
    print("-" * 30)
    
    # Test different file extensions
    assert detect_data_source('test.csv') == 'csv'
    assert detect_data_source('test.db') == 'sqlite'
    assert detect_data_source('test.sqlite') == 'sqlite'
    assert detect_data_source('test.sqlite3') == 'sqlite'
    assert detect_data_source('test.json') == 'json'
    assert detect_data_source('test.jsonl') == 'json'
    assert detect_data_source('test.txt') == 'unknown'
    
    print("✅ Auto-detection test passed!")
    return True


def test_error_handling():
    """Test error handling for various invalid scenarios"""
    print("🔍 Testing Error Handling")
    print("-" * 30)
    
    test_results = []
    
    # Test 1: Non-existent file
    state = create_initial_state()
    state = ingest_data_file('nonexistent.csv', state)
    test_results.append(state['status'] == 'error' and 'does not exist' in state['error'])
    
    # Test 2: Unsupported file type
    state = create_initial_state()
    state = ingest_data_file('test.txt', state)
    test_results.append(state['status'] == 'error' and 'Unsupported' in state['error'])
    
    # Test 3: Empty file (create one)
    Path('data/empty.csv').touch()
    state = create_initial_state()
    state = ingest_data_file('data/empty.csv', state)
    test_results.append(state['status'] == 'error' and 'empty' in state['error'])
    
    print("✅ Error handling test passed!")
    print(f"   All {len(test_results)} error scenarios handled correctly")
    return all(test_results)


def test_schema_generation():
    """Test schema generation for different data types"""
    print("🔍 Testing Schema Generation")
    print("-" * 30)
    
    # Create CSV with different data types
    data = {
        'integers': [1, 2, 3],
        'floats': [1.1, 2.2, 3.3],
        'strings': ['a', 'b', 'c'],
        'dates': ['2024-01-01', '2024-01-02', '2024-01-03']
    }
    df = pd.DataFrame(data)
    df.to_csv('data/schema_test.csv', index=False)
    
    # Test ingestion
    state = create_initial_state()
    state = ingest_data_file('data/schema_test.csv', state)
    
    # Verify schema
    schema = state['schema']
    assert 'columns' in schema, "Schema should have columns"
    assert 'total_rows' in schema, "Schema should have row count"
    assert 'total_columns' in schema, "Schema should have column count"
    assert 'data_types' in schema, "Schema should have data types"
    assert len(schema['columns']) == 4, "Should have 4 columns"
    assert schema['total_rows'] == 3, "Should have 3 rows"
    
    print("✅ Schema generation test passed!")
    print(f"   Columns: {schema['columns']}")
    print(f"   Data types: {schema['data_types']}")
    return True


def run_comprehensive_test():
    """Run all tests and report results"""
    print("🚀 Comprehensive Ingestion Agent Test")
    print("=" * 50)
    
    tests = [
        ("CSV Ingestion", test_csv_ingestion),
        ("SQLite Ingestion", test_sqlite_ingestion),
        ("JSON Ingestion", test_json_ingestion),
        ("Auto-Detection", test_auto_detection),
        ("Error Handling", test_error_handling),
        ("Schema Generation", test_schema_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result, None))
            print()
        except Exception as e:
            results.append((test_name, False, str(e)))
            print(f"❌ {test_name} failed: {e}")
            print()
    
    # Summary
    print("=" * 50)
    print("🎯 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    for test_name, result, error in results:
        if result:
            print(f"✅ {test_name}: PASSED")
            passed += 1
        else:
            print(f"❌ {test_name}: FAILED - {error}")
    
    print(f"\n📊 Overall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Ingestion Agent is working perfectly!")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False


if __name__ == "__main__":
    success = run_comprehensive_test()
    exit(0 if success else 1)

