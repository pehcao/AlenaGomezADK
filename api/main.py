#!/usr/bin/env python3
"""
ADK Sales Agent API - Domain-driven architecture
Main application entry point
"""

import sys
import os
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Add parent directory to sys.path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from api.core.config import settings
from api.core.exceptions import ADKBaseException
from api.services.airtable.routes import router as airtable_router
from api.services.airtable.schemas import AirtableSchemaManager

# Initialize FastAPI app with new architecture
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include service routers
app.include_router(airtable_router)

@app.get("/")
async def health_check():
    """
    Health check endpoint
    """
    return JSONResponse({
        "status": "healthy",
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "timestamp": datetime.now().isoformat(),
        "architecture": "Domain-Driven Design v2.0"
    })

@app.get("/schemas")
async def get_schemas():
    """
    Get information about available table schemas
    """
    try:
        schema_manager = AirtableSchemaManager()
        schemas_info = schema_manager.get_schema_info()
        
        return JSONResponse({
            "success": True,
            "available_tables": schema_manager.get_available_tables(),
            "schemas": schemas_info,
            "total_tables": len(schemas_info)
        })
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Error retrieving schemas: {str(e)}",
            "schemas": {},
            "total_tables": 0
        })

@app.get("/config")
async def get_config():
    """
    Get application configuration (non-sensitive data)
    """
    return JSONResponse({
        "success": True,
        "config": settings.get_all_settings(),
        "message": "Application configuration retrieved successfully"
    })

# Global exception handler for custom exceptions
@app.exception_handler(ADKBaseException)
async def adk_exception_handler(request: Request, exc: ADKBaseException):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": exc.message,
            "error_code": exc.error_code,
            "details": exc.details
        }
    )

# Global exception handler for uncaught exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "An unexpected error occurred",
            "error_code": "INTERNAL_ERROR",
            "details": {"error": str(exc)} if settings.DEBUG else {}
        }
    )

# Error handling for common HTTP errors
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": "Endpoint not found",
            "error_code": "NOT_FOUND"
        }
    )

@app.exception_handler(405)
async def method_not_allowed_handler(request: Request, exc):
    return JSONResponse(
        status_code=405,
        content={
            "success": False,
            "message": "Method not allowed",
            "error_code": "METHOD_NOT_ALLOWED"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    ) 