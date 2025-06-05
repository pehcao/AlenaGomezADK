# Tests Directory

This directory contains all test files for the ADK Sales Agent application.

## 🧪 Test Files

### `test_standardized_client.py`
**Comprehensive test suite for core functionality**

Tests the following components:
- ✅ Configuration validation (`Config` class)
- ✅ AirtableClient CRUD operations (get_all, create, update, delete, search)
- ✅ SalesOperations business logic layer
- ✅ Full integration testing with live Airtable data

**Usage:**
```bash
cd tests
python test_standardized_client.py
```

**Test Suites:**
1. **Configuration Test**: Validates environment variables and config setup
2. **AirtableClient Test**: Tests basic CRUD operations and data access
3. **SalesOperations Test**: Tests business logic methods like `get_lead_by_phone` 
4. **CRUD Operations Test**: Full create → update → delete cycle with cleanup

### `test_table_schemas.py`
**Complete Airtable schema extraction and documentation**

Extracts detailed schema information for all tables including:
- ✅ All fields (35 in Leads, 20 in Calls) - even empty ones
- ✅ Field types, IDs, and configuration options
- ✅ Comparison between schema fields vs. fields with actual data
- ✅ JSON export of complete schemas

**Usage:**
```bash
cd tests  
python test_table_schemas.py
```

**Outputs:**
- `../schemas/schema_leads_table.json` - Complete leads table schema
- `../schemas/schema_calls_table.json` - Complete calls table schema  
- `../schemas/complete_airtable_schema.json` - Combined schema file

## 🚀 Running Tests

### Individual Tests
```bash
# Run specific test
cd tests
python test_standardized_client.py
python test_table_schemas.py
```

### All Tests
```bash
# Run from project root
python -m pytest tests/ -v
```

## 📋 Test Requirements

All tests require:
- Valid `.env` file with `AIRTABLE_API_KEY`
- Proper Airtable base and table IDs in config
- Internet connection for Airtable API calls

## 🔧 Test Data

Tests use live Airtable data but include proper cleanup:
- Create operations are always followed by delete operations
- Test records are clearly marked (e.g., "Standardized Test Lead")
- No permanent changes to production data 