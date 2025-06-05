#!/usr/bin/env python3
"""
Airtable-specific Pydantic models
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

# Request Models
class CreateRecordRequest(BaseModel):
    table: str = Field(..., description="Table name (e.g., 'leads_table', 'calls_table')")
    fields: Optional[Dict[str, Any]] = Field(None, description="Record fields to set")

class UpdateRecordRequest(BaseModel):
    table: str = Field(..., description="Table name")
    record_id: str = Field(..., description="Record ID to update")
    fields: Dict[str, Any] = Field(..., description="Fields to update")

class DeleteRecordRequest(BaseModel):
    table: str = Field(..., description="Table name")
    record_id: str = Field(..., description="Record ID to delete")

class GetRecordRequest(BaseModel):
    table: str = Field(..., description="Table name")
    record_id: str = Field(..., description="Record ID to retrieve")

class SearchRecordRequest(BaseModel):
    table: str = Field(..., description="Table name")
    field: str = Field(..., description="Field name to search")
    value: str = Field(..., description="Value to search for")

# Response Models
class CreateRecordResponse(BaseModel):
    success: bool
    record_id: Optional[str] = None
    message: str
    created_fields: Optional[Dict[str, Any]] = None
    validation_errors: Optional[List[str]] = None

class UpdateRecordResponse(BaseModel):
    success: bool
    record_id: Optional[str] = None
    message: str
    updated_fields: Optional[Dict[str, Any]] = None
    validation_errors: Optional[List[str]] = None

class DeleteRecordResponse(BaseModel):
    success: bool
    message: str
    deleted_record_id: Optional[str] = None

class GetRecordResponse(BaseModel):
    success: bool
    record_id: Optional[str] = None
    record: Optional[Dict[str, Any]] = None
    message: str

class GetRecordsResponse(BaseModel):
    success: bool
    records: List[Dict[str, Any]]
    total_count: int
    message: str

class SearchRecordResponse(BaseModel):
    success: bool
    records: List[Dict[str, Any]]
    total_found: int
    message: str

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

# Domain-specific models
class Lead(BaseModel):
    """Lead model representing a sales prospect"""
    id: Optional[str] = None
    name: Optional[str] = None
    lead_phone_number: Optional[str] = None
    alcaldia: Optional[str] = None
    direccion: Optional[str] = None
    referencias: Optional[str] = None
    cuantas_persons: Optional[int] = None
    status: Optional[str] = None
    num_llamadas: Optional[int] = None
    contactado: Optional[str] = None
    monto: Optional[str] = None

class Call(BaseModel):
    """Call model representing a sales call"""
    id: Optional[str] = None
    call_id: Optional[str] = None
    lead_name: Optional[str] = None
    lead_phone_number: Optional[str] = None
    call_type: Optional[str] = None
    transcript: Optional[str] = None
    call_datetime: Optional[str] = None 