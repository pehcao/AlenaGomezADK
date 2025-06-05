"""
Simplified configuration for ADK Sales Agent
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for ADK Sales Agent"""
    
    # Airtable Configuration (Required)
    AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY")
    AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID", "appYKRoIWJLctlUdw")
    AIRTABLE_LEADS_TABLE_ID = os.environ.get("AIRTABLE_LEADS_TABLE_ID", "tblUZkxzC0MbJ12HG")
    AIRTABLE_CALLS_TABLE_ID = os.environ.get("AIRTABLE_CALLS_TABLE_ID", "tblCalls")


    @classmethod
    def validate_required_env_vars(cls):
        """Validate that all required environment variables are set"""
        # Only validate Airtable for now - OpenAI is optional depending on features used
        required_vars = [
            ("AIRTABLE_API_KEY", cls.AIRTABLE_API_KEY)
        ]
        
        missing_vars = [var_name for var_name, var_value in required_vars if not var_value]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
    
    @classmethod
    def get_table_config(cls):
        """Get table configuration for easy access"""
        return {
            "leads_table": cls.AIRTABLE_LEADS_TABLE_ID,
            "calls_table": cls.AIRTABLE_CALLS_TABLE_ID,
            "base_id": cls.AIRTABLE_BASE_ID
        } 