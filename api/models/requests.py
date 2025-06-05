#!/usr/bin/env python3
"""
Pydantic models for API requests and responses
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel

# Request Models
class CreateRecordRequest(BaseModel):
    table: str
    fields: Optional[Dict[str, Any]] = None

class UpdateRecordRequest(BaseModel):
    table: str
    record_id: str
    fields: Dict[str, Any]

class DeleteRecordRequest(BaseModel):
    table: str
    record_id: str

class GetRecordRequest(BaseModel):
    table: str
    record_id: str

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

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None 