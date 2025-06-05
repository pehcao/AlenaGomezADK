#!/usr/bin/env python3
"""
Airtable repository - Data access layer
"""

import os
import sys
from typing import Dict, Any, List, Optional

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from app.airtable_client import AirtableClient
from api.core.exceptions import ExternalServiceError, ResourceNotFoundError
from api.services.airtable.schemas import TableMapper

class AirtableRepository:
    """Repository for Airtable data access operations"""
    
    def __init__(self, client: AirtableClient):
        self.client = client
        self.table_mapper = TableMapper()
    
    def _get_table_id(self, table_name: str) -> str:
        """Get actual table ID from table name"""
        return self.table_mapper.get_table_id(table_name)
    
    async def create_record(self, table_name: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record"""
        try:
            table_id = self._get_table_id(table_name)
            result = self.client.create(table_id, fields)
            
            if not result:
                raise ExternalServiceError("Airtable", "Failed to create record")
            
            return result
            
        except Exception as e:
            if isinstance(e, (ExternalServiceError, ValueError)):
                raise
            raise ExternalServiceError("Airtable", f"Create operation failed: {str(e)}")
    
    async def get_record(self, table_name: str, record_id: str) -> Dict[str, Any]:
        """Get a specific record by ID"""
        try:
            table_id = self._get_table_id(table_name)
            result = self.client.get(table_id, record_id)
            
            if not result:
                raise ResourceNotFoundError("Record", record_id)
            
            return result
            
        except Exception as e:
            if isinstance(e, (ResourceNotFoundError, ValueError)):
                raise
            raise ExternalServiceError("Airtable", f"Get operation failed: {str(e)}")
    
    async def get_all_records(self, table_name: str, **kwargs) -> List[Dict[str, Any]]:
        """Get all records from a table"""
        try:
            table_id = self._get_table_id(table_name)
            result = self.client.get_all(table_id, **kwargs)
            return result or []
            
        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise ExternalServiceError("Airtable", f"Get all operation failed: {str(e)}")
    
    async def update_record(self, table_name: str, record_id: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing record"""
        try:
            table_id = self._get_table_id(table_name)
            result = self.client.update(table_id, record_id, fields)
            
            if not result:
                raise ResourceNotFoundError("Record", record_id)
            
            return result
            
        except Exception as e:
            if isinstance(e, (ResourceNotFoundError, ValueError)):
                raise
            raise ExternalServiceError("Airtable", f"Update operation failed: {str(e)}")
    
    async def delete_record(self, table_name: str, record_id: str) -> bool:
        """Delete a record"""
        try:
            table_id = self._get_table_id(table_name)
            result = self.client.delete(table_id, record_id)
            return bool(result)
            
        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise ExternalServiceError("Airtable", f"Delete operation failed: {str(e)}")
    
    async def search_records(self, table_name: str, field: str, value: str) -> List[Dict[str, Any]]:
        """Search for records by field value"""
        try:
            table_id = self._get_table_id(table_name)
            result = self.client.search(table_id, field, value)
            return result or []
            
        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise ExternalServiceError("Airtable", f"Search operation failed: {str(e)}")
    
    async def find_first_record(self, table_name: str, field: str, value: str) -> Optional[Dict[str, Any]]:
        """Find first record matching criteria"""
        try:
            table_id = self._get_table_id(table_name)
            result = self.client.find_first(table_id, field, value)
            return result
            
        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise ExternalServiceError("Airtable", f"Find operation failed: {str(e)}") 