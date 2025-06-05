#!/usr/bin/env python3
"""
Comprehensive test script for the ADK Sales Agent API
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_endpoint(name, method, url, data=None):
    """Test an API endpoint and display results"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    
    try:
        if method.upper() == "GET":
            response = requests.get(f"{API_BASE}{url}")
        elif method.upper() == "POST":
            response = requests.post(f"{API_BASE}{url}", json=data)
        elif method.upper() == "PUT":
            response = requests.put(f"{API_BASE}{url}", json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(f"{API_BASE}{url}", json=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response:")
        
        try:
            result = response.json()
            print(json.dumps(result, indent=2))
            return result
        except:
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Run comprehensive API tests"""
    print("🚀 ADK Sales Agent API - Comprehensive Test Suite")
    print("=" * 60)
    
    # 1. Health Check
    test_endpoint("Health Check", "GET", "/")
    
    # 2. Configuration
    test_endpoint("Configuration", "GET", "/config")
    
    # 3. Schemas
    test_endpoint("Table Schemas", "GET", "/schemas")
    
    # 4. Create a Lead
    lead_data = {
        "table": "leads_table",
        "fields": {
            "name": "María González Test",
            "lead_phone_number": "525512345999",
            "alcaldia": "Benito Juárez",
            "direccion": "Av. Insurgentes Sur 123",
            "cuantas_persons": 4,
            "status": "nuevo_lead"
        }
    }
    create_result = test_endpoint("Create Lead", "POST", "/airtable/create-record", lead_data)
    
    if create_result and create_result.get("success"):
        record_id = create_result.get("record_id")
        
        # 5. Get the created record
        test_endpoint("Get Created Record", "GET", f"/airtable/record/leads_table/{record_id}")
        
        # 6. Update the record
        update_data = {
            "table": "leads_table",
            "record_id": record_id,
            "fields": {
                "status": "contactado",
                "num_llamadas": 1,
                "contactado": "Si"
            }
        }
        test_endpoint("Update Lead", "PUT", "/airtable/update-record", update_data)
        
        # 7. Get updated record
        test_endpoint("Get Updated Record", "GET", f"/airtable/record/leads_table/{record_id}")
        
        # 8. Test business logic endpoint - get lead by phone
        test_endpoint("Get Lead by Phone", "GET", f"/airtable/leads/by-phone/525512345999")
        
        # 9. Clean up - delete the test record
        delete_data = {
            "table": "leads_table",
            "record_id": record_id
        }
        test_endpoint("Delete Test Record", "DELETE", "/airtable/delete-record", delete_data)
    
    # 10. Get all leads (limited view)
    all_leads = test_endpoint("Get All Leads", "GET", "/airtable/records/leads_table")
    
    # 11. Test validation errors
    invalid_data = {
        "table": "leads_table",
        "fields": {
            "invalid_field": "should fail",
            "cuantas_persons": "not a number"  # Should be a number
        }
    }
    test_endpoint("Test Validation Errors", "POST", "/airtable/create-record", invalid_data)
    
    # 12. Test invalid table
    invalid_table_data = {
        "table": "nonexistent_table",
        "fields": {"name": "test"}
    }
    test_endpoint("Test Invalid Table", "POST", "/airtable/create-record", invalid_table_data)
    
    print(f"\n{'='*60}")
    print("✅ Test suite completed!")
    print("🌐 Visit http://localhost:8000/docs for interactive API documentation")
    print("=" * 60)

if __name__ == "__main__":
    main() 