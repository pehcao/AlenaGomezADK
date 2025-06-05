#!/usr/bin/env python3
"""
Common validation helpers for Airtable service
"""

from typing import List, Tuple
from api.services.airtable.schemas import AirtableSchemaManager


class AirtableValidator:
    """Common validation helpers for Airtable operations"""
    
    def __init__(self, schema_manager: AirtableSchemaManager):
        self.schema_manager = schema_manager
    
    def validate_table_and_fields(self, table_name: str, fields: dict = None) -> Tuple[bool, List[str], str]:
        """
        Validate table name and optional fields
        
        Returns:
            Tuple of (is_valid, errors, message)
        """
        errors = []
        
        # Validate table name
        if not self.schema_manager.validate_table_name(table_name):
            available_tables = self.schema_manager.get_available_tables()
            errors.append(f"Unknown table: {table_name}")
            return False, errors, f"Invalid table '{table_name}'. Available tables: {', '.join(available_tables)}"
        
        # Validate fields if provided
        if fields:
            field_errors = self.schema_manager.validate_fields(table_name, fields)
            if field_errors:
                errors.extend(field_errors)
                return False, errors, "Field validation failed"
        
        return True, [], "Validation passed"
    
    def get_available_tables_message(self) -> str:
        """Get formatted message with available tables"""
        tables = self.schema_manager.get_available_tables()
        return f"Available tables: {', '.join(tables)}" 