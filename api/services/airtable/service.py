#!/usr/bin/env python3
"""
Airtable service - Business logic layer
"""

import os
import sys
from typing import Dict, Any, List, Optional

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from api.services.airtable.repository import AirtableRepository
from api.services.airtable.models import (
    CreateRecordRequest, CreateRecordResponse,
    UpdateRecordRequest, UpdateRecordResponse,
    DeleteRecordRequest, DeleteRecordResponse,
    GetRecordResponse, GetRecordsResponse,
    SearchRecordRequest, SearchRecordResponse
)
from api.services.airtable.schemas import AirtableSchemaManager
from api.services.airtable.validators import AirtableValidator
from api.core.exceptions import ValidationError, ServiceError

class AirtableService:
    """Service layer for Airtable business logic"""
    
    def __init__(self, repository: AirtableRepository, schema_manager: AirtableSchemaManager):
        self.repository = repository
        self.schema_manager = schema_manager
        self.validator = AirtableValidator(schema_manager)
    
    async def create_record(self, request: CreateRecordRequest) -> CreateRecordResponse:
        """Create a new record with validation"""
        try:
            # Validate table and fields
            is_valid, validation_errors, message = self.validator.validate_table_and_fields(
                request.table, request.fields
            )
            if not is_valid:
                return CreateRecordResponse(
                    success=False,
                    message=message,
                    validation_errors=validation_errors
                )
            
            # Create the record
            fields_to_create = request.fields or {}
            result = await self.repository.create_record(request.table, fields_to_create)
            
            return CreateRecordResponse(
                success=True,
                record_id=result.get("id"),
                message=f"Successfully created record {result.get('id')}",
                created_fields=request.fields
            )
            
        except Exception as e:
            return CreateRecordResponse(
                success=False,
                message=f"Error creating record: {str(e)}"
            )
    
    async def get_record(self, table_name: str, record_id: str) -> GetRecordResponse:
        """Get a specific record by ID"""
        try:
            # Validate table name
            if not self.schema_manager.validate_table_name(table_name):
                available_tables = self.schema_manager.get_available_tables()
                return GetRecordResponse(
                    success=False,
                    message=f"Invalid table '{table_name}'. Available tables: {', '.join(available_tables)}"
                )
            
            # Get the record
            record = await self.repository.get_record(table_name, record_id)
            
            return GetRecordResponse(
                success=True,
                record_id=record_id,
                record=record,
                message=f"Successfully retrieved record {record_id}"
            )
            
        except Exception as e:
            return GetRecordResponse(
                success=False,
                message=f"Error retrieving record: {str(e)}"
            )
    
    async def get_all_records(self, table_name: str) -> GetRecordsResponse:
        """Get all records from a table"""
        try:
            # Validate table name
            if not self.schema_manager.validate_table_name(table_name):
                available_tables = self.schema_manager.get_available_tables()
                return GetRecordsResponse(
                    success=False,
                    records=[],
                    total_count=0,
                    message=f"Invalid table '{table_name}'. Available tables: {', '.join(available_tables)}"
                )
            
            # Get all records
            records = await self.repository.get_all_records(table_name)
            
            return GetRecordsResponse(
                success=True,
                records=records,
                total_count=len(records),
                message=f"Successfully retrieved {len(records)} records"
            )
            
        except Exception as e:
            return GetRecordsResponse(
                success=False,
                records=[],
                total_count=0,
                message=f"Error retrieving records: {str(e)}"
            )
    
    async def update_record(self, request: UpdateRecordRequest) -> UpdateRecordResponse:
        """Update an existing record"""
        try:
            # Validate table and fields
            is_valid, validation_errors, message = self.validator.validate_table_and_fields(
                request.table, request.fields
            )
            if not is_valid:
                return UpdateRecordResponse(
                    success=False,
                    message=message,
                    validation_errors=validation_errors
                )
            
            # Update the record
            result = await self.repository.update_record(request.table, request.record_id, request.fields)
            
            return UpdateRecordResponse(
                success=True,
                record_id=request.record_id,
                message=f"Successfully updated record {request.record_id}",
                updated_fields=request.fields
            )
            
        except Exception as e:
            return UpdateRecordResponse(
                success=False,
                message=f"Error updating record: {str(e)}"
            )
    
    async def delete_record(self, request: DeleteRecordRequest) -> DeleteRecordResponse:
        """Delete a record"""
        try:
            # Validate table name
            if not self.schema_manager.validate_table_name(request.table):
                available_tables = self.schema_manager.get_available_tables()
                return DeleteRecordResponse(
                    success=False,
                    message=f"Invalid table '{request.table}'. Available tables: {', '.join(available_tables)}"
                )
            
            # Delete the record
            success = await self.repository.delete_record(request.table, request.record_id)
            
            if success:
                return DeleteRecordResponse(
                    success=True,
                    message=f"Successfully deleted record {request.record_id}",
                    deleted_record_id=request.record_id
                )
            else:
                return DeleteRecordResponse(
                    success=False,
                    message="Failed to delete record"
                )
                
        except Exception as e:
            return DeleteRecordResponse(
                success=False,
                message=f"Error deleting record: {str(e)}"
            )
    
    async def search_records(self, request: SearchRecordRequest) -> SearchRecordResponse:
        """Search for records by field value"""
        try:
            # Validate table name
            if not self.schema_manager.validate_table_name(request.table):
                available_tables = self.schema_manager.get_available_tables()
                return SearchRecordResponse(
                    success=False,
                    records=[],
                    total_found=0,
                    message=f"Invalid table '{request.table}'. Available tables: {', '.join(available_tables)}"
                )
            
            # Search for records
            records = await self.repository.search_records(request.table, request.field, request.value)
            
            return SearchRecordResponse(
                success=True,
                records=records,
                total_found=len(records),
                message=f"Found {len(records)} records matching '{request.field}' = '{request.value}'"
            )
            
        except Exception as e:
            return SearchRecordResponse(
                success=False,
                records=[],
                total_found=0,
                message=f"Error searching records: {str(e)}"
            )
    
    # Business logic methods
    async def get_lead_by_phone(self, phone: str) -> Optional[Dict[str, Any]]:
        """Get lead by phone number (business logic)"""
        try:
            return await self.repository.find_first_record("leads_table", "lead_phone_number", phone)
        except Exception as e:
            raise ServiceError("AirtableService", f"Failed to get lead by phone: {str(e)}")
    
    async def create_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new lead (business logic)"""
        try:
            return await self.repository.create_record("leads_table", lead_data)
        except Exception as e:
            raise ServiceError("AirtableService", f"Failed to create lead: {str(e)}")
    
    async def update_lead_status(self, record_id: str, status: str) -> Dict[str, Any]:
        """Update lead status (business logic)"""
        try:
            return await self.repository.update_record("leads_table", record_id, {"status": status})
        except Exception as e:
            raise ServiceError("AirtableService", f"Failed to update lead status: {str(e)}")
    
    async def create_call(self, call_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a call record (business logic)"""
        try:
            return await self.repository.create_record("calls_table", call_data)
        except Exception as e:
            raise ServiceError("AirtableService", f"Failed to create call: {str(e)}") 