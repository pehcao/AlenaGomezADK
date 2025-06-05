#!/usr/bin/env python3
"""
Airtable schema management and validation
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from api.core.exceptions import ValidationError, ConfigurationError


class AirtableSchemaManager:
    """Manages Airtable table schemas and validation"""
    
    def __init__(self):
        self.schemas = self._load_schemas()
    
    def _load_schemas(self) -> Dict[str, Dict]:
        """Load table schemas from JSON files"""
        schemas = {}
        schema_dir = self._get_schema_directory()
        
        try:
            # Load leads table schema
            leads_path = os.path.join(schema_dir, "schema_leads_table.json")
            if os.path.exists(leads_path):
                with open(leads_path, 'r') as f:
                    schemas['leads_table'] = json.load(f)
            
            # Load calls table schema
            calls_path = os.path.join(schema_dir, "schema_calls_table.json")
            if os.path.exists(calls_path):
                with open(calls_path, 'r') as f:
                    schemas['calls_table'] = json.load(f)
                    
        except Exception as e:
            raise ConfigurationError(f"Failed to load schemas: {e}")
            
        return schemas
    
    def _get_schema_directory(self) -> str:
        """Get the schema directory path"""
        # Go up from api/services/airtable/ to project root, then to schemas/
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        return os.path.join(project_root, "schemas")
    
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
        if table_name not in self.schemas:
            raise ValidationError(f"Unknown table: {table_name}")
        
        errors = []
        valid_fields = self.get_table_fields(table_name)
        
        # Check each provided field
        for field_name, field_value in fields.items():
            if field_name not in valid_fields:
                errors.append(f"Unknown field '{field_name}' for table '{table_name}'")
                continue
            
            # Validate field type
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


class TableMapper:
    """Maps logical table names to actual Airtable table IDs"""
    
    TABLE_MAPPING = {
        "leads_table": "tblUZkxzC0MbJ12HG",
        "calls_table": "tblyyuYfdzGc0CAkO"
    }
    
    @classmethod
    def get_table_id(cls, table_name: str) -> str:
        """Get actual table ID from logical table name"""
        if table_name not in cls.TABLE_MAPPING:
            raise ValidationError(f"Unknown table: {table_name}")
        return cls.TABLE_MAPPING[table_name]
    
    @classmethod
    def get_available_tables(cls) -> List[str]:
        """Get list of available logical table names"""
        return list(cls.TABLE_MAPPING.keys()) 