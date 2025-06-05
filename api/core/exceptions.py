#!/usr/bin/env python3
"""
Custom exception classes for the ADK Sales Agent API
"""

from typing import Optional, Dict, Any

class ADKBaseException(Exception):
    """Base exception class for ADK Sales Agent API"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(ADKBaseException):
    """Raised when data validation fails"""
    
    def __init__(self, message: str, field_errors: Optional[Dict[str, str]] = None):
        super().__init__(message, "VALIDATION_ERROR")
        self.field_errors = field_errors or {}

class ServiceError(ADKBaseException):
    """Raised when a service operation fails"""
    
    def __init__(self, service_name: str, message: str, original_error: Optional[Exception] = None):
        super().__init__(f"{service_name}: {message}", "SERVICE_ERROR")
        self.service_name = service_name
        self.original_error = original_error

class ResourceNotFoundError(ADKBaseException):
    """Raised when a requested resource is not found"""
    
    def __init__(self, resource_type: str, resource_id: str):
        message = f"{resource_type} with ID '{resource_id}' not found"
        super().__init__(message, "RESOURCE_NOT_FOUND")
        self.resource_type = resource_type
        self.resource_id = resource_id

class AuthenticationError(ADKBaseException):
    """Raised when authentication fails"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "AUTHENTICATION_ERROR")

class AuthorizationError(ADKBaseException):
    """Raised when authorization fails"""
    
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, "AUTHORIZATION_ERROR")

class ExternalServiceError(ADKBaseException):
    """Raised when an external service (Airtable, Google, etc.) fails"""
    
    def __init__(self, service_name: str, message: str, status_code: Optional[int] = None):
        super().__init__(f"{service_name} error: {message}", "EXTERNAL_SERVICE_ERROR")
        self.service_name = service_name
        self.status_code = status_code

class ConfigurationError(ADKBaseException):
    """Raised when there's a configuration problem"""
    
    def __init__(self, message: str):
        super().__init__(message, "CONFIGURATION_ERROR") 