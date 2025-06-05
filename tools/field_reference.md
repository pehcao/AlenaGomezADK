# Leads Table Field Reference

Complete field breakdown from `schema_leads_table.json` (35 total fields)

## ✅ First Half - Used in `create_sample_lead.py` (18 fields)

| # | Field Name | Type | Purpose | Sample Data |
|---|------------|------|---------|-------------|
| 1 | `lead_phone_number` | singleLineText | Phone number (key field) | "555-DEMO-2024" |
| 2 | `folio` | number | Sequential ID/folio number | 12345 |
| 3 | `name` | singleLineText | Lead's full name | "María González Demo" |
| 4 | `alcaldia` | singleLineText | Municipality/district | "Benito Juárez" |
| 5 | `direccion` | multilineText | Full address | "Av. Insurgentes Sur 1234\nCol. Del Valle..." |
| 6 | `referencias` | multilineText | Address references | "Edificio azul, segundo piso..." |
| 7 | `lugar_de_prospeccion` | singleLineText | Where lead was found | "Feria de Salud CDMX" |
| 8 | `cuantas_persons` | number | Number of people | 4 |
| 9 | `actores` | multilineText | Key people/decision makers | "María González (decisora principal)..." |
| 10 | `fecha_follow_up` | dateTime | Next follow-up date | "2025-06-07 19:49" |
| 11 | `num_llamadas` | number (precision 2) | Total calls made | 0.0 |
| 12 | `contactado` | singleLineText | Contact status | "Pendiente" |
| 13 | `last_whatsapp_reachout_datetime` | dateTime | Last WhatsApp contact | "2025-06-04 19:49" |
| 14 | `num_llamadas_incompletas` | number (precision 2) | Incomplete calls | 0.0 |
| 15 | `llamada_completa` | singleLineText | Complete call status | "No" |
| 16 | `fecha_cita` | dateTime | Appointment date | "2025-06-09 19:49" |
| 17 | `status` | singleLineText | Current lead status | "Nuevo Lead" |
| 18 | `regalo` | singleLineText | Gift/incentive offered | "Consulta nutricional gratuita" |

## 📋 Second Half - Available for Extension (17 fields)

| # | Field Name | Type | Purpose |
|---|------------|------|---------|
| 19 | `entregado` | singleLineText | Delivery status |
| 20 | `Insumos` | singleLineText | Supplies/materials |
| 21 | `venta` | singleLineText | Sale status |
| 22 | `monto` | singleLineText | Sale amount |
| 23 | `comision` | singleLineText | Commission |
| 24 | `Platillo` | singleLineText | Dish/product |
| 25 | `Prospecto` | singleLineText | Prospect classification |
| 26 | `Observaciones` | singleLineText | General observations |
| 27 | `last_update` | dateTime | Last update timestamp |
| 28 | `update_source` | singleLineText | Source of last update |
| 29 | `conversation_history` | multilineText | AI conversation history |
| 30 | `openai_thread_id` | singleLineText | OpenAI thread identifier |
| 31 | `followup_task_id` | singleLineText | Task management ID |
| 32 | `followups_today` | number (precision 1) | Daily follow-up count |
| 33 | `last_voice_call_datetime` | singleLineText | Last voice call time |
| 34 | `last_conversation_id` | singleLineText | Last conversation ID |
| 35 | `voice_calls_today` | number (precision 1) | Daily voice call count |

## 🎯 Field Categories

### 📞 Contact & Communication
- `lead_phone_number`, `contactado`, `last_whatsapp_reachout_datetime`
- `num_llamadas`, `num_llamadas_incompletas`, `llamada_completa`
- `last_voice_call_datetime`, `voice_calls_today`

### 📍 Location & Address
- `alcaldia`, `direccion`, `referencias`, `lugar_de_prospeccion`

### 👥 People & Relationships
- `name`, `cuantas_persons`, `actores`

### 📅 Scheduling & Follow-ups
- `fecha_follow_up`, `fecha_cita`, `followups_today`, `followup_task_id`

### 💼 Sales & Business
- `folio`, `status`, `regalo`, `venta`, `monto`, `comision`, `Platillo`, `entregado`, `Insumos`

### 🤖 AI & Automation
- `openai_thread_id`, `conversation_history`, `last_conversation_id`

### 📊 Tracking & Analytics
- `last_update`, `update_source`, `Prospecto`, `Observaciones`

## 💡 Usage Examples

### Creating with Second Half Fields
```python
# Additional fields you could add to create_sample_lead.py
additional_data = {
    "venta": "Pendiente",
    "monto": "$2,500 MXN", 
    "Platillo": "Plan Nutricional Básico",
    "conversation_history": "Contacto inicial realizado por WhatsApp\nInterés mostrado en consulta nutricional",
    "openai_thread_id": "thread_abc123...",
    "last_update": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "update_source": "create_sample_lead.py script"
}
```

### Business Workflow Fields
```python
# For advanced lead management
workflow_data = {
    "followup_task_id": "task_12345",
    "followups_today": 0,
    "voice_calls_today": 0,
    "Prospecto": "Caliente",
    "Observaciones": "Familia interesada, seguimiento programado"
}
```

## 🔧 Field Type Reference

- **singleLineText**: Short text (name, status, phone)
- **multilineText**: Long text with line breaks (address, notes, history)  
- **number**: Numeric values with precision settings
- **dateTime**: Date/time with timezone and format options

## 📈 Schema Statistics

- **Total Fields**: 35
- **Used in Demo**: 18 (51%)
- **Available for Extension**: 17 (49%)
- **Field Types**: 4 different types
- **DateTime Fields**: 6 total (scheduling, tracking, automation) 