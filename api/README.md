# ADK Sales Agent API

A domain-driven FastAPI application for managing Airtable records with schema validation.

## 🏗️ Architecture

This API follows a clean, modular architecture with clear separation of concerns:

```
api/
├── main.py                     # 🚀 Main FastAPI app initialization
├── models/                    # 📝 Pydantic models
│   ├── __init__.py
│   └── requests.py           # Request/response models
├── routes/                    # 🛣️  API endpoints
│   ├── __init__.py
│   └── airtable.py          # Airtable CRUD operations
└── utils/                     # 🔧 Utility modules
    ├── __init__.py
    └── schema_validator.py   # Schema validation logic
```

## 🚀 Quick Start

### Option 1: Using main.py (Domain-Driven Architecture)
```bash
cd api
python main.py
```

### Option 2: Using uvicorn directly
```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Endpoints

### Core Endpoints
- `GET /` - Health check
- `GET /schemas` - Get table schemas and field information
- `GET /docs` - Interactive API documentation

### Airtable Operations
- `POST /airtable/create-record` - Create new records
- `GET /airtable/record/{table_name}/{record_id}` - Get specific record
- `GET /airtable/records/{table_name}` - Get all records from table
- `PUT /airtable/update-record` - Update existing record
- `DELETE /airtable/delete-record` - Delete record

## 🔧 Features

### ✅ Schema Validation
- Automatic validation against extracted Airtable schemas
- Field type checking (string, number, datetime, email, etc.)
- Helpful error messages for invalid data

### 🏗️ Modular Design
- **Separation of Concerns**: Routes, models, and utilities in separate modules
- **Scalable**: Easy to add new endpoints and functionality
- **Maintainable**: Clear code organization and documentation

### 📊 Complete CRUD Operations
- **Create**: Add new records with validation
- **Read**: Retrieve individual or all records
- **Update**: Modify existing records
- **Delete**: Remove records

### 🎯 Type Safety
- Pydantic models for request/response validation
- Type hints throughout the codebase
- Automatic API documentation generation

## 📝 Example Requests

### Create a Lead
```bash
curl -X POST "http://localhost:8000/airtable/create-record" \
  -H "Content-Type: application/json" \
  -d '{
    "table": "leads_table",
    "fields": {
      "nombre": "María González",
      "telefono": "525538899800",
      "email": "maria@empresa.com"
    }
  }'
```

### Get All Leads
```bash
curl "http://localhost:8000/airtable/records/leads_table"
```

### Update a Record
```bash
curl -X PUT "http://localhost:8000/airtable/update-record" \
  -H "Content-Type: application/json" \
  -d '{
    "table": "leads_table",
    "record_id": "recXXXXXXXXX",
    "fields": {
      "nombre": "María González Updated"
    }
  }'
```

## 🛠️ Development

### Adding New Endpoints
1. Add new models to `models/requests.py`
2. Create routes in `routes/airtable.py` or new route file
3. Include router in `main.py`

### Schema Updates
The schema validator automatically loads schemas from the `/schemas` directory. No code changes needed when schemas are updated.

## 📋 Available Tables
- `leads_table` - Customer leads and prospects (35 fields)
- `calls_table` - Call logs and communication history (20 fields)

## 🔍 Interactive Documentation
Visit `http://localhost:8000/docs` for Swagger UI with live API testing. 