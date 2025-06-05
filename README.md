# ADK Sales Agent

A comprehensive FastAPI-based sales agent application with Airtable integration, built using clean architecture principles.

## 🚀 Features

- **Dual Architecture**: WhatsApp agent (main.py) + Clean FastAPI API (api/)
- **Airtable Integration**: Full CRUD operations with schema validation
- **Domain-Driven Design**: Modern, scalable architecture following SOLID principles
- **Comprehensive Testing**: Full test suite with 100% endpoint coverage
- **Interactive Documentation**: Auto-generated API docs with Swagger UI
- **Environment-Based Configuration**: Secure configuration management

## 📁 Project Structure

```
ADKSalesAgent/
├── main.py                    # WhatsApp Agent (legacy)
├── api/                       # FastAPI Application
│   ├── main.py               # API entry point
│   ├── core/                 # Core configurations
│   ├── services/             # Business logic
│   │   └── airtable/         # Airtable domain
│   │       ├── models.py     # Data models
│   │       ├── schemas.py    # Schema management
│   │       ├── validators.py # Validation helpers
│   │       ├── repository.py # Data access layer
│   │       ├── service.py    # Business logic
│   │       └── routes.py     # HTTP endpoints
│   └── models/               # Shared models
├── test_api.py               # Comprehensive test suite
├── requirements.txt          # Dependencies
└── .env.example             # Environment template
```

## 🔧 Quick Start

### 🚀 Automated Setup (Recommended)

**Linux/macOS:**
```bash
git clone <repository-url>
cd ADKSalesAgent
./setup.sh
```

**Windows:**
```cmd
git clone <repository-url>
cd ADKSalesAgent
setup.bat
```

The setup script automatically:
- ✅ Checks Python 3.8+ installation
- ✅ Creates and activates virtual environment
- ✅ Installs all dependencies
- ✅ Sets up environment configuration
- ✅ Runs connectivity tests
- ✅ Provides next steps

### ⚙️ Manual Setup

### 1. Clone & Setup
```bash
git clone <repository-url>
cd ADKSalesAgent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your Airtable credentials
```

### 3. Run the API
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗂️ API Endpoints

### Core Endpoints
- `GET /` - Health check
- `GET /schemas` - Available table schemas
- `GET /config` - Application configuration

### Generic CRUD (prefix: `/airtable`)
- `POST /airtable/create-record` - Create record
- `GET /airtable/record/{table}/{id}` - Get record by ID
- `GET /airtable/records/{table}` - Get all records
- `PUT /airtable/update-record` - Update record
- `DELETE /airtable/delete-record` - Delete record
- `POST /airtable/search-records` - Search records

### Business Logic
- `GET /airtable/leads/by-phone/{phone}` - Find lead by phone
- `POST /airtable/leads/create` - Create lead with validation
- `PUT /airtable/leads/{id}/status` - Update lead status

## 🔐 Configuration

### Required Environment Variables
```bash
# Airtable (Required)
AIRTABLE_API_KEY=your_api_key_here
AIRTABLE_BASE_ID=your_base_id
AIRTABLE_LEADS_TABLE_ID=your_leads_table_id
AIRTABLE_CALLS_TABLE_ID=your_calls_table_id
```

### Optional Variables
```bash
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Future integrations
OPENAI_API_KEY=your_openai_key
WHATSAPP_ACCESS_TOKEN=your_whatsapp_token
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_api.py
```

Tests include:
- Health check validation
- CRUD operations
- Error handling
- Schema validation
- Business logic endpoints

## 🏗️ Architecture

### Clean Architecture Principles
- **Domain-Driven Design**: Clear separation of concerns
- **SOLID Principles**: Single responsibility, dependency inversion
- **Layered Architecture**: Routes → Service → Repository → External APIs

### Data Flow
```
HTTP Request → FastAPI → Routes → Service → Validator → Repository → Airtable API
```

### Key Components
- **Models**: Pydantic data validation
- **Schemas**: Table structure management
- **Validators**: Common validation logic
- **Repository**: Data access abstraction
- **Service**: Business logic layer
- **Routes**: HTTP endpoint handlers

## 📦 Dependencies

Core packages:
- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **python-dotenv**: Environment management
- **pyairtable**: Airtable API client

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the existing architecture patterns
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

[Add your license information here]

## 🔗 Links

- [Airtable API Documentation](https://airtable.com/developers/web/api/introduction)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)

---

Built with ❤️ using modern Python practices and clean architecture principles.