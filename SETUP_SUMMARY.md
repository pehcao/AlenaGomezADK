# 🚀 ADK Sales Agent API - Setup Summary

## 📋 Application Overview

The **ADK Sales Agent API** is a comprehensive FastAPI application for managing Airtable records with schema validation. It features both a legacy architecture (`main.py`) and a modern domain-driven design architecture (`main_v2.py`).

## 🏗️ Architecture Summary

### Current Architecture

**Domain-Driven Architecture** (`api/main.py`) ⭐
- Clean separation of concerns
- Service/Repository pattern  
- Dependency injection
- Scalable for future features
- Custom exception handling

## 📁 Project Structure

```
ADKSalesAgent/
├── api/                          # API application code
│   ├── main.py                   # Domain-driven FastAPI app
│   ├── core/                    # Core application concerns
│   │   ├── config.py           # Centralized configuration
│   │   ├── dependencies.py     # Dependency injection
│   │   └── exceptions.py       # Custom exceptions
│   ├── services/                # Domain-specific services
│   │   └── airtable/           # Airtable service domain
│   │       ├── models.py       # Pydantic models
│   │       ├── service.py      # Business logic
│   │       ├── repository.py   # Data access layer
│   │       └── routes.py       # API endpoints
│   ├── models/                  # Legacy Pydantic models
│   ├── routes/                  # Legacy API routes
│   └── utils/                   # Utility modules
├── app/                         # Core application modules
│   └── airtable_client.py      # Airtable API client
├── config/                      # Configuration files
│   └── config.py               # Application configuration
├── schemas/                     # Airtable table schemas
│   ├── schema_leads_table.json
│   └── schema_calls_table.json
├── requirements.txt             # Python dependencies
├── test_api.py                 # Comprehensive test suite
└── .env                        # Environment variables
```

## ⚙️ Environment Setup

### Required Environment Variables

Create a `.env` file with the following variables:

```env
# Airtable Configuration (Required)
AIRTABLE_API_KEY=your_airtable_api_key_here
AIRTABLE_BASE_ID=appYKRoIWJLctlUdw
AIRTABLE_LEADS_TABLE_ID=tblUZkxzC0MbJ12HG
AIRTABLE_CALLS_TABLE_ID=tblyyuYfdzGc0CAkO

# API Configuration
DEBUG=true
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

## 🚀 Getting Started

### 1. Install Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Install requirements (already done)
pip install -r requirements.txt
```

### 2. Start the API Server

#### Option 1: Domain-Driven Architecture (Recommended)
```bash
cd api
python main_v2.py
```

#### Option 2: Legacy Architecture
```bash
cd api
python main.py
```

#### Option 3: Using the runner script
```bash
cd api
python run_server.py
```

### 3. Verify Installation

```bash
# Run comprehensive test suite
python test_api.py
```

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Core Endpoints

#### Health & Configuration
- `GET /` - Health check
- `GET /config` - Application configuration
- `GET /schemas` - Table schemas and field information

#### Airtable Operations
- `POST /airtable/create-record` - Create new records
- `GET /airtable/record/{table_name}/{record_id}` - Get specific record
- `GET /airtable/records/{table_name}` - Get all records from table
- `PUT /airtable/update-record` - Update existing record
- `DELETE /airtable/delete-record` - Delete record

#### Business Logic (v2.0 only)
- `GET /airtable/leads/by-phone/{phone}` - Get lead by phone number
- `POST /airtable/leads/create` - Create new lead
- `PUT /airtable/leads/{record_id}/status` - Update lead status

## 📊 Available Tables

### Leads Table (`leads_table`)
- **35 fields** including:
  - `name` - Lead name
  - `lead_phone_number` - Phone number
  - `alcaldia` - Municipality
  - `direccion` - Address
  - `status` - Lead status
  - `cuantas_persons` - Number of people
  - `num_llamadas` - Number of calls

### Calls Table (`calls_table`)
- **20 fields** including:
  - `call_id` - Unique call identifier
  - `lead_name` - Associated lead name
  - `lead_phone_number` - Phone number
  - `call_type` - Type of call
  - `transcript` - Call transcript
  - `call_datetime` - Call timestamp

## 🛠️ Features

### ✅ Schema Validation
- Automatic validation against Airtable schemas
- Field type checking (string, number, datetime, email)
- Helpful error messages for invalid data

### 🏗️ Domain-Driven Design (v2.0)
- **Service Layer**: Business logic separation
- **Repository Pattern**: Data access abstraction
- **Dependency Injection**: Loose coupling
- **Custom Exceptions**: Structured error handling

### 📝 Type Safety
- Pydantic models for request/response validation
- Type hints throughout codebase
- Automatic API documentation generation

## 🧪 Testing

### Comprehensive Test Suite
```bash
python test_api.py
```

Tests include:
- Health check and configuration
- CRUD operations (Create, Read, Update, Delete)
- Schema validation
- Business logic endpoints
- Error handling

### Example API Calls

#### Create a Lead
```bash
curl -X POST "http://localhost:8000/airtable/create-record" \
  -H "Content-Type: application/json" \
  -d '{
    "table": "leads_table",
    "fields": {
      "name": "María González",
      "lead_phone_number": "525538899800",
      "alcaldia": "Benito Juárez",
      "cuantas_persons": 4
    }
  }'
```

#### Get Lead by Phone
```bash
curl "http://localhost:8000/airtable/leads/by-phone/525538899800"
```

## 🏗️ Architecture Benefits

The domain-driven architecture provides:
- Better separation of concerns
- Easier testing and mocking
- Scalability for future services
- Cleaner error handling
- Business logic endpoints for complex operations

## 🎯 Next Steps

### Future Enhancements (Architecture Ready)
1. **Google Calendar Integration** - Appointment scheduling
2. **WhatsApp Service** - Message automation
3. **OpenAI Service** - AI-powered interactions
4. **Advanced Analytics** - Lead scoring and insights

### Development Guidelines
1. Use the v2.0 architecture for new features
2. Follow the service/repository pattern
3. Add comprehensive tests for new endpoints
4. Maintain schema validation for data integrity

## ✅ Verification Checklist

- [x] Virtual environment activated
- [x] Dependencies installed
- [x] Environment variables configured
- [x] API server running (port 8000)
- [x] Airtable connection established
- [x] Schema validation working
- [x] CRUD operations functional
- [x] Test suite passing
- [x] Interactive documentation accessible

## 🎉 Status: **FULLY INITIALIZED & OPERATIONAL**

The ADK Sales Agent API is now ready for development and production use. Both architecture versions are available, with the domain-driven v2.0 recommended for scalability and maintainability. 