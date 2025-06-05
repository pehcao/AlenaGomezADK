#!/usr/bin/env python3
"""
Dependency injection container for the ADK Sales Agent API
"""

import os
import sys
from typing import Dict, Any, Callable, TypeVar, Type
from functools import lru_cache

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from api.core.config import settings
from api.core.exceptions import ConfigurationError

T = TypeVar('T')

class DependencyContainer:
    """Simple dependency injection container"""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
    
    def register_singleton(self, service_name: str, instance: Any) -> None:
        """Register a singleton instance"""
        self._services[service_name] = instance
    
    def register_factory(self, service_name: str, factory: Callable) -> None:
        """Register a factory function for creating instances"""
        self._factories[service_name] = factory
    
    def get(self, service_name: str) -> Any:
        """Get a service instance"""
        # Check if singleton exists
        if service_name in self._services:
            return self._services[service_name]
        
        # Check if factory exists
        if service_name in self._factories:
            instance = self._factories[service_name]()
            # Cache as singleton after first creation
            self._services[service_name] = instance
            return instance
        
        raise ConfigurationError(f"Service '{service_name}' not registered")
    
    def get_or_create(self, service_class: Type[T], *args, **kwargs) -> T:
        """Get or create an instance of a service class"""
        service_name = service_class.__name__
        
        if service_name not in self._services:
            instance = service_class(*args, **kwargs)
            self._services[service_name] = instance
        
        return self._services[service_name]

# Global dependency container
container = DependencyContainer()

# Factory functions for creating service instances

def create_airtable_client():
    """Factory for creating Airtable client"""
    from app.airtable_client import AirtableClient
    return AirtableClient(base_id=settings.AIRTABLE_BASE_ID)

def create_airtable_sales_operations():
    """Factory for creating Airtable sales operations"""
    from app.airtable_client import SalesOperations
    client = get_airtable_client()
    return SalesOperations(
        client=client,
        leads_table=settings.AIRTABLE_LEADS_TABLE_ID,
        calls_table=settings.AIRTABLE_CALLS_TABLE_ID
    )

def create_schema_validator():
    """Factory for creating schema validator"""
    from api.utils.schema_validator import SchemaValidator
    return SchemaValidator()

# Register factories
container.register_factory("airtable_client", create_airtable_client)
container.register_factory("airtable_sales_operations", create_airtable_sales_operations)
container.register_factory("schema_validator", create_schema_validator)

# FastAPI dependency functions

@lru_cache()
def get_airtable_client():
    """Get Airtable client dependency"""
    return container.get("airtable_client")

@lru_cache()
def get_airtable_sales_operations():
    """Get Airtable sales operations dependency"""
    return container.get("airtable_sales_operations")

@lru_cache()
def get_schema_validator():
    """Get schema validator dependency"""
    return container.get("schema_validator")

def get_settings():
    """Get application settings dependency"""
    return settings

# Dependency registration for future services

def register_calendar_service():
    """Register Google Calendar service (when implemented)"""
    # TODO: Implement when calendar service is added
    pass

def register_whatsapp_service():
    """Register WhatsApp service (when implemented)"""
    # TODO: Implement when WhatsApp service is added
    pass

def register_openai_service():
    """Register OpenAI service (when implemented)"""
    # TODO: Implement when OpenAI service is added
    pass 