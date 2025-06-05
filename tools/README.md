# Tools Directory

This directory contains utility scripts and diagnostic tools for the ADK Sales Agent application.

## 🔧 Utility Scripts

### `check_permissions.py`
**Airtable API permissions and token diagnostic tool**

This tool helps diagnose and troubleshoot Airtable API access issues:

- ✅ **Token Type Detection**: Identifies Personal Access Token (PAT) vs Legacy API Key
- ✅ **Permission Testing**: Tests READ, CREATE, UPDATE, DELETE permissions
- ✅ **Error Diagnosis**: Provides specific guidance for common permission issues
- ✅ **Setup Validation**: Confirms your API token has proper access to your base

**Usage:**
```bash
cd tools
python check_permissions.py
```

**What it tests:**
1. **Token Format Analysis**: Detects token type and format
2. **READ Test**: Attempts to fetch records from leads table
3. **WRITE Tests**: Creates, updates, and deletes a test record
4. **Permission Troubleshooting**: Provides actionable guidance for fixing issues

**Sample Output:**
```
🔐 Checking Airtable API Permissions
==================================================

🔍 API Token Analysis:
   ✅ Personal Access Token (PAT) detected
   📝 This is the newer, recommended token type
   📝 Token starts with: patMqo8Qto...

🔍 Testing READ permissions:
   ✅ READ: Success - found 4 records

🔧 Testing WRITE permissions:
   ✅ CREATE: Success - created record recXXXXXXXXXXXXXX
   ✅ UPDATE: Success  
   ✅ DELETE: Success - cleaned up test record
```

**Troubleshooting Help:**
When issues are detected, the tool provides detailed guidance for:
- Creating Personal Access Tokens with proper scopes
- Configuring base access permissions
- Fixing common authentication errors
- Setting up legacy API keys (if needed)

## 🚀 Running Tools

```bash
# From tools directory
cd tools
python check_permissions.py

# From project root
python tools/check_permissions.py
```

## 📋 Tool Requirements

- Valid `.env` file with `AIRTABLE_API_KEY`
- Internet connection for Airtable API calls
- Proper Airtable base and table configuration

## 🔧 When to Use

Use `check_permissions.py` when:
- Setting up the project for the first time
- Troubleshooting "401 Unauthorized" or "403 Forbidden" errors
- Switching from Legacy API Key to Personal Access Token
- Verifying API access after token changes
- Diagnosing permission-related issues

### `create_sample_lead.py`
**Sample lead creation using schema-based field mapping**

This script demonstrates how to create new leads using the complete field schema:

- ✅ **Schema-Based Creation**: Uses first 18 fields from `schema_leads_table.json`
- ✅ **Proper Data Types**: Demonstrates `singleLineText`, `multilineText`, `number`, `dateTime`
- ✅ **Realistic Data**: Creates business-relevant sample data
- ✅ **SalesOperations Integration**: Tests the created lead with business logic layer
- ✅ **Cleanup Options**: Optionally removes demo data after testing

**Usage:**
```bash
cd tools
python create_sample_lead.py
```

**What it creates:**
- Complete lead record with 18 fields populated
- Realistic Mexican business data (addresses, names, locations)
- Proper date/time fields with future follow-up dates
- Multiline text fields with formatted addresses and references
- Integration testing with SalesOperations layer

**Sample Output:**
```
🆕 Creating Sample Lead - First Half of Schema Fields
============================================================
📋 Target table: tblUZkxzC0MbJ12HG

📝 Lead data to be created:
----------------------------------------
   lead_phone_number              (singleLineText ): 555-DEMO-2024
   folio                          (number         ): 12345
   name                           (singleLineText ): María González Demo
   alcaldia                       (singleLineText ): Benito Juárez
   direccion                      (multilineText  ): Av. Insurgentes Sur 1234...

✅ Lead created successfully!
📋 Record ID: recXXXXXXXXXXXXXX
📊 Fields saved (18 total)
```

**Fields Demonstrated:**
1. **Basic Info**: `lead_phone_number`, `name`, `folio`
2. **Location**: `alcaldia`, `direccion`, `referencias`
3. **Business Logic**: `lugar_de_prospeccion`, `status`, `contactado`
4. **Numbers**: `cuantas_persons`, `num_llamadas`, `num_llamadas_incompletas`
5. **Dates**: `fecha_follow_up`, `fecha_cita`, `last_whatsapp_reachout_datetime`
6. **Complex Text**: `actores`, `regalo`

### `update_manuel_gonzalez.py`
**Comprehensive record update demonstrating field reset and randomization**

This script showcases advanced update operations using the complete schema:

- ✅ **Record Search**: Finds specific records by name with fallback partial matching
- ✅ **Field Reset**: Resets first 18 fields to 0/empty values (preserving key fields)
- ✅ **Random Data Generation**: Populates last 17 fields with realistic random values
- ✅ **Comprehensive Schema Usage**: Demonstrates all 35 fields from `schema_leads_table.json`
- ✅ **Safety Confirmation**: Asks for user confirmation before making changes
- ✅ **Verification**: Tests updates with SalesOperations layer

**Usage:**
```bash
cd tools
python update_manuel_gonzalez.py
```

**What it does:**
1. **Searches** for Manuel Gonzalez record (exact + partial matching)
2. **Resets** first half fields: `folio`, `alcaldia`, `direccion`, etc. → 0/empty
3. **Randomizes** second half fields: `venta`, `monto`, `Prospecto`, etc. → realistic data
4. **Preserves** key fields: `name`, `lead_phone_number` (essential for identification)
5. **Verifies** the update using SalesOperations layer

**Sample Random Data Generated:**
- **Sales**: "En proceso", "$2,500 MXN", "15%"
- **Products**: "Plan Nutricional Básico", "Kit completo"
- **AI Integration**: OpenAI thread IDs, conversation history
- **Workflow**: Task IDs, follow-up counts, voice call metrics
- **Business Logic**: Prospect classifications, observations

**Fields Updated:**
- **Reset (18 fields)**: Core contact info, location, call counts → 0/empty
- **Randomized (17 fields)**: Sales data, AI fields, workflow metrics → realistic values

**Sample Output:**
```
🔍 Searching for Manuel Gonzalez record...
✅ Found record: recVlabTk2EzvybTy
📋 Name: Manuel Gonzalez
📞 Phone: 525538899800

🔄 FIRST HALF - Reset to 0/empty:
   folio                         = 0
   alcaldia                      = 
   num_llamadas                  = 0.0

🎲 SECOND HALF - Random realistic values:
   venta                         = En proceso
   monto                         = $2,500 MXN
   Prospecto                     = Muy Interesado
   openai_thread_id              = thread_123456abc
``` 