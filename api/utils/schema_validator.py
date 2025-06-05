#!/usr/bin/env python3
"""
Schema validation utilities for Airtable table schemas
"""

import os
import json
from typing import Dict, Any, Optional, List
from datetime import datetime

class SchemaValidator:
    """Validates fields against Airtable table schemas"""
    
    def __init__(self):
        self.schemas = self._load_schemas()
    
    def _load_schemas(self) -> Dict[str, Dict]:
        """Load table schemas from JSON files"""
        schemas = {}
        # Go up two levels from api/utils/ to get to project root, then to schemas/
        schema_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            "schemas"
        )
        
        try:
            # Load leads table schema
            leads_path = os.path.join(schema_dir, "schema_leads_table.json")
            if os.path.exists(leads_path):
                with open(leads_path, 'r') as f:
                    leads_schema = json.load(f)
                    schemas['leads_table'] = leads_schema
            
            # Load calls table schema
            calls_path = os.path.join(schema_dir, "schema_calls_table.json")
            if os.path.exists(calls_path):
                with open(calls_path, 'r') as f:
                    calls_schema = json.load(f)
                    schemas['calls_table'] = calls_schema
                    
        except Exception as e:
            print(f"Warning: Could not load schemas: {e}")
            
        return schemas
    
    def get_table_fields(self, table_name: str) -> Dict[str, str]:
        """Get field names and types for a table"""
        if table_name not in self.schemas:
            return {}
        
        fields = {}
        for field in self.schemas[table_name].get('fields', []):
            fields[field['name']] = field['type']
        
        return fields
    
    def get_available_tables(self) -> List[str]:
        """Get list of available table names"""
        return list(self.schemas.keys())
    
    def get_schema_info(self) -> Dict[str, Dict]:
        """Get schema information for all tables"""
        schemas_info = {}
        for table_name, schema in self.schemas.items():
            schemas_info[table_name] = {
                "total_fields": schema.get("total_fields", 0),
                "fields": [
                    {
                        "name": field["name"],
                        "type": field["type"],
                        "id": field["id"]
                    }
                    for field in schema.get("fields", [])
                ]
            }
        return schemas_info
    
    def validate_table_name(self, table_name: str) -> bool:
        """Check if table name is valid"""
        return table_name in self.schemas
    
    def validate_fields(self, table_name: str, fields: Dict[str, Any]) -> List[str]:
        """Validate fields against table schema"""
        errors = []
        
        if table_name not in self.schemas:
            errors.append(f"Unknown table: {table_name}")
            return errors
        
        # Get valid fields for this table
        valid_fields = self.get_table_fields(table_name)
        
        # Check each provided field
        for field_name, field_value in fields.items():
            if field_name not in valid_fields:
                errors.append(f"Unknown field '{field_name}' for table '{table_name}'")
                continue
            
            # Validate field type (basic validation)
            field_type = valid_fields[field_name]
            validation_error = self._validate_field_type(field_name, field_value, field_type)
            if validation_error:
                errors.append(validation_error)
        
        return errors
    
    def _validate_field_type(self, field_name: str, value: Any, expected_type: str) -> Optional[str]:
        """Validate a single field against its expected type"""
        if value is None:
            return None  # Allow null values
        
        try:
            if expected_type == "singleLineText":
                if not isinstance(value, str):
                    return f"Field '{field_name}' must be a string (got {type(value).__name__})"
            
            elif expected_type == "multilineText":
                if not isinstance(value, str):
                    return f"Field '{field_name}' must be a string (got {type(value).__name__})"
            
            elif expected_type == "number":
                if not isinstance(value, (int, float)):
                    return f"Field '{field_name}' must be a number (got {type(value).__name__})"
            
            elif expected_type == "dateTime":
                if isinstance(value, str):
                    # Try to parse the datetime string
                    try:
                        datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except ValueError:
                        return f"Field '{field_name}' must be a valid ISO datetime string"
                else:
                    return f"Field '{field_name}' must be a datetime string (got {type(value).__name__})"
            
            elif expected_type == "email":
                if not isinstance(value, str) or '@' not in value:
                    return f"Field '{field_name}' must be a valid email address"
            
            elif expected_type == "phoneNumber":
                if not isinstance(value, str):
                    return f"Field '{field_name}' must be a phone number string (got {type(value).__name__})"
            
        except Exception as e:
            return f"Validation error for field '{field_name}': {str(e)}"
        
        return None 