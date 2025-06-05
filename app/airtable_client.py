"""
Clean Airtable client - simplified and consistent API design
"""

import os
import sys
from pyairtable import Api

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import Config


class AirtableClient:
    """Simple, consistent client for Airtable operations"""
    
    def __init__(self, base_id: str = None):
        """Initialize the client
        
        Args:
            base_id: Airtable base ID (uses config default if not provided)
        """
        if not Config.AIRTABLE_API_KEY:
            raise ValueError("AIRTABLE_API_KEY is required but not set")
            
        self.api = Api(Config.AIRTABLE_API_KEY)
        self.base_id = base_id or Config.AIRTABLE_BASE_ID
        self._table_cache = {}
    
    def _get_table(self, table_id: str):
        """Get or create a table object (with caching)"""
        cache_key = f"{self.base_id}:{table_id}"
        if cache_key not in self._table_cache:
            self._table_cache[cache_key] = self.api.table(self.base_id, table_id)
        return self._table_cache[cache_key]
    
    # ===== CORE CRUD OPERATIONS =====
    
    def get_all(self, table_id: str, **kwargs):
        """Get all records from a table"""
        try:
            table = self._get_table(table_id)
            return table.all(**kwargs)
        except Exception as e:
            print(f"❌ Error fetching records from {table_id}: {e}")
            return []
    
    def get(self, table_id: str, record_id: str):
        """Get a specific record by ID"""
        try:
            table = self._get_table(table_id)
            return table.get(record_id)
        except Exception as e:
            print(f"❌ Error fetching record {record_id}: {e}")
            return None
    
    def create(self, table_id: str, fields: dict):
        """Create a new record"""
        try:
            table = self._get_table(table_id)
            result = table.create(fields)
            print(f"✅ Created record in {table_id}: {result['id']}")
            return result
        except Exception as e:
            print(f"❌ Error creating record in {table_id}: {e}")
            return None
    
    def update(self, table_id: str, record_id: str, fields: dict):
        """Update a record"""
        try:
            table = self._get_table(table_id)
            result = table.update(record_id, fields)
            print(f"✅ Updated {table_id} record {record_id}")
            return result
        except Exception as e:
            print(f"❌ Error updating record {record_id}: {e}")
            return None
    
    def delete(self, table_id: str, record_id: str):
        """Delete a record"""
        try:
            table = self._get_table(table_id)
            result = table.delete(record_id)
            print(f"✅ Deleted record {record_id}")
            return result
        except Exception as e:
            print(f"❌ Error deleting record {record_id}: {e}")
            return None
    
    def search(self, table_id: str, field: str, value: str):
        """Search for records by field value"""
        try:
            table = self._get_table(table_id)
            # Get all records and filter in Python to avoid formula issues
            all_records = table.all()
            print(f"🔍 Debug: Got {len(all_records)} total records from {table_id}")
            
            matching_records = []
            for record in all_records:
                if record.get('fields', {}).get(field) == value:
                    matching_records.append(record)
                    print(f"🔍 Debug: Found match - {field}: {record.get('fields', {}).get(field)}")
            
            print(f"🔍 Debug: Found {len(matching_records)} matching records")
            return matching_records
        except Exception as e:
            print(f"❌ Error searching {table_id}: {e}")
            return []
    
    def find_first(self, table_id: str, field: str, value: str):
        """Find first record matching criteria (common use case)"""
        results = self.search(table_id, field, value)
        return results[0] if results else None


# ===== OPTIONAL: Business Logic Layer =====

class SalesOperations:
    """Higher-level operations for sales workflow"""
    
    def __init__(self, client: AirtableClient, leads_table: str, calls_table: str):
        self.client = client
        self.leads_table = leads_table
        self.calls_table = calls_table
    
    def get_lead_by_phone(self, phone: str):
        """Get lead by phone number"""
        return self.client.find_first(self.leads_table, "lead_phone_number", phone)
    
    def create_lead(self, lead_data: dict):
        """Create a new lead"""
        return self.client.create(self.leads_table, lead_data)
    
    def update_lead_status(self, record_id: str, status: str):
        """Update lead status"""
        return self.client.update(self.leads_table, record_id, {"Status": status})
    
    def create_call(self, call_data: dict):
        """Create a call record"""
        return self.client.create(self.calls_table, call_data)
    
    def get_lead_with_calls(self, phone: str):
        """Get lead with all associated calls"""
        lead = self.get_lead_by_phone(phone)
        calls = self.client.search(self.calls_table, "lead_phone_number", phone)
        
        return {
            "lead": lead,
            "calls": calls,
            "total_calls": len(calls)
        } if lead else None 