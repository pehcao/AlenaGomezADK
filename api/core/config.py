#!/usr/bin/env python3
"""
Centralized configuration for the ADK Sales Agent API
"""

import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Load environment variables
load_dotenv()

class Settings:
    """Centralized application settings"""
    
    # API Configuration
    API_TITLE: str = "ADK Sales Agent API"
    API_DESCRIPTION: str = "API for managing Airtable records with schema validation"
    API_VERSION: str = "2.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Airtable Configuration
    AIRTABLE_API_KEY: str = os.getenv("AIRTABLE_API_KEY", "")
    AIRTABLE_BASE_ID: str = os.getenv("AIRTABLE_BASE_ID", "appYKRoIWJLctlUdw")
    AIRTABLE_LEADS_TABLE_ID: str = os.getenv("AIRTABLE_LEADS_TABLE_ID", "tblUZkxzC0MbJ12HG")
    AIRTABLE_CALLS_TABLE_ID: str = os.getenv("AIRTABLE_CALLS_TABLE_ID", "tblyyuYfdzGc0CAkO")
    
    # Google Calendar Configuration (for future use)
    GOOGLE_CALENDAR_CREDENTIALS_FILE: str = os.getenv("GOOGLE_CALENDAR_CREDENTIALS_FILE", "")
    GOOGLE_CALENDAR_ID: str = os.getenv("GOOGLE_CALENDAR_ID", "")
    
    # WhatsApp Configuration (for future use)
    WHATSAPP_ACCESS_TOKEN: str = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
    WHATSAPP_PHONE_NUMBER_ID: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    WHATSAPP_WEBHOOK_VERIFY_TOKEN: str = os.getenv("WHATSAPP_WEBHOOK_VERIFY_TOKEN", "")
    
    # OpenAI Configuration (for future use)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_ASSISTANT_ID: str = os.getenv("OPENAI_ASSISTANT_ID", "")
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def validate_required_settings(cls) -> None:
        """Validate that all required settings are present"""
        required_settings = [
            ("AIRTABLE_API_KEY", cls.AIRTABLE_API_KEY, "Airtable API key is required"),
        ]
        
        missing_settings = []
        for setting_name, setting_value, error_message in required_settings:
            if not setting_value:
                missing_settings.append(f"{setting_name}: {error_message}")
        
        if missing_settings:
            raise ValueError(f"Missing required settings:\n" + "\n".join(missing_settings))
    
    @classmethod
    def get_airtable_config(cls) -> Dict[str, str]:
        """Get Airtable configuration as a dictionary"""
        return {
            "api_key": cls.AIRTABLE_API_KEY,
            "base_id": cls.AIRTABLE_BASE_ID,
            "leads_table_id": cls.AIRTABLE_LEADS_TABLE_ID,
            "calls_table_id": cls.AIRTABLE_CALLS_TABLE_ID,
        }
    
    @classmethod
    def get_all_settings(cls) -> Dict[str, Any]:
        """Get all settings as a dictionary (excluding sensitive data)"""
        return {
            "api_title": cls.API_TITLE,
            "api_version": cls.API_VERSION,
            "debug": cls.DEBUG,
            "host": cls.HOST,
            "port": cls.PORT,
            "log_level": cls.LOG_LEVEL,
            "airtable_base_id": cls.AIRTABLE_BASE_ID,
            "airtable_leads_table_id": cls.AIRTABLE_LEADS_TABLE_ID,
            "airtable_calls_table_id": cls.AIRTABLE_CALLS_TABLE_ID,
        }

# Global settings instance
settings = Settings()

# Validate settings on import
settings.validate_required_settings() 