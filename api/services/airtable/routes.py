#!/usr/bin/env python3
"""
Airtable API routes using the new service architecture
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from api.services.airtable.models import (
    CreateRecordRequest, CreateRecordResponse,
    UpdateRecordRequest, UpdateRecordResponse,
    DeleteRecordRequest, DeleteRecordResponse,
    GetRecordResponse, GetRecordsResponse,
    SearchRecordRequest, SearchRecordResponse
)
from api.services.airtable.service import AirtableService
from api.services.airtable.repository import AirtableRepository
from api.services.airtable.schemas import AirtableSchemaManager
from api.core.dependencies import get_airtable_client

# Create router
router = APIRouter(prefix="/airtable", tags=["airtable"])

def get_airtable_service(
    client=Depends(get_airtable_client)
) -> AirtableService:
    """Dependency to get AirtableService instance"""
    repository = AirtableRepository(client)
    schema_manager = AirtableSchemaManager()
    return AirtableService(repository, schema_manager)

@router.post("/create-record", response_model=CreateRecordResponse)
async def create_record(
    request: CreateRecordRequest,
    service: AirtableService = Depends(get_airtable_service)
):
    """
    Create a new record in the specified Airtable table with optional field validation
    """
    return await service.create_record(request)

@router.get("/record/{table_name}/{record_id}", response_model=GetRecordResponse)
async def get_record(
    table_name: str,
    record_id: str,
    service: AirtableService = Depends(get_airtable_service)
):
    """
    Get a specific record by ID from the specified table
    """
    return await service.get_record(table_name, record_id)

@router.get("/records/{table_name}", response_model=GetRecordsResponse)
async def get_all_records(
    table_name: str,
    service: AirtableService = Depends(get_airtable_service)
):
    """
    Get all records from the specified table
    """
    return await service.get_all_records(table_name)

@router.put("/update-record", response_model=UpdateRecordResponse)
async def update_record(
    request: UpdateRecordRequest,
    service: AirtableService = Depends(get_airtable_service)
):
    """
    Update an existing record in the specified table
    """
    return await service.update_record(request)

@router.delete("/delete-record", response_model=DeleteRecordResponse)
async def delete_record(
    request: DeleteRecordRequest,
    service: AirtableService = Depends(get_airtable_service)
):
    """
    Delete a record from the specified table
    """
    return await service.delete_record(request)

@router.post("/search-records", response_model=SearchRecordResponse)
async def search_records(
    request: SearchRecordRequest,
    service: AirtableService = Depends(get_airtable_service)
):
    """
    Search for records by field value
    """
    return await service.search_records(request)

# Business logic endpoints
@router.get("/leads/by-phone/{phone}")
async def get_lead_by_phone(
    phone: str,
    service: AirtableService = Depends(get_airtable_service)
):
    """
    Get lead by phone number (business logic)
    """
    try:
        lead = await service.get_lead_by_phone(phone)
        if lead:
            return {"success": True, "lead": lead}
        else:
            return {"success": False, "message": f"No lead found with phone {phone}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/leads/create")
async def create_lead(
    lead_data: Dict[str, Any],
    service: AirtableService = Depends(get_airtable_service)
):
    """
    Create a new lead (business logic)
    """
    try:
        result = await service.create_lead(lead_data)
        return {"success": True, "lead": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/leads/{record_id}/status")
async def update_lead_status(
    record_id: str,
    status: str,
    service: AirtableService = Depends(get_airtable_service)
):
    """
    Update lead status (business logic)
    """
    try:
        result = await service.update_lead_status(record_id, status)
        return {"success": True, "updated_lead": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 