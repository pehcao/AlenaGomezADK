#!/usr/bin/env python3
"""
Test the standardized AirtableClient with simplified configuration
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent directory to Python path  
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.airtable_client import AirtableClient, SalesOperations
from config.config import Config

def test_config():
    """Test the simplified configuration"""
    print("🔧 Testing Simplified Configuration")
    print("=" * 50)
    
    try:
        # Test config validation
        Config.validate_required_env_vars()
        print("✅ Required environment variables validated")
        
        # Show config values
        print(f"📋 Base ID: {Config.AIRTABLE_BASE_ID}")
        print(f"📋 Leads Table: {Config.AIRTABLE_LEADS_TABLE_ID}")
        print(f"📋 Calls Table: {Config.AIRTABLE_CALLS_TABLE_ID}")
        
        # Test table config helper
        table_config = Config.get_table_config()
        print(f"📋 Table Config: {table_config}")
        
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_standardized_client():
    """Test the standardized AirtableClient"""
    print("\n🧪 Testing Standardized AirtableClient")
    print("=" * 50)
    
    try:
        # Initialize client
        client = AirtableClient()
        print("✅ Client initialized successfully")
        
        # Get table config
        config = Config.get_table_config()
        leads_table = config['leads_table']
        calls_table = config['calls_table']
        
        print(f"📋 Using leads table: {leads_table}")
        print(f"📋 Using calls table: {calls_table}")
        
        # Test basic operations
        print("\n🔍 Testing READ operations...")
        
        # Get all leads
        leads = client.get_all(leads_table)
        print(f"   ✅ Found {len(leads)} leads")
        
        if leads:
            # Test search
            sample_phone = leads[0]['fields'].get('lead_phone_number')
            if sample_phone:
                found = client.find_first(leads_table, "lead_phone_number", sample_phone)
                if found:
                    print(f"   ✅ Search working: found {found['fields']['name']}")
                else:
                    print("   ❌ Search failed")
                    
        # Test calls table (if accessible)
        try:
            calls = client.get_all(calls_table)
            print(f"   ✅ Found {len(calls)} calls")
        except Exception as e:
            print(f"   ⚠️  Calls table: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Client test failed: {e}")
        return False

def test_sales_operations():
    """Test the SalesOperations layer"""
    print("\n🎯 Testing SalesOperations")
    print("=" * 50)
    
    try:
        # Get table config
        config = Config.get_table_config()
        
        # Initialize client and sales operations
        client = AirtableClient()
        sales = SalesOperations(
            client, 
            config['leads_table'], 
            config['calls_table']
        )
        
        print("✅ SalesOperations initialized successfully")
        
        # Test operations
        leads = client.get_all(config['leads_table'])
        
        if leads:
            sample_phone = leads[0]['fields'].get('lead_phone_number')
            if sample_phone:
                # Test get_lead_by_phone
                lead = sales.get_lead_by_phone(sample_phone)
                if lead:
                    print(f"   ✅ get_lead_by_phone: found {lead['fields']['name']}")
                    
                    # Test get_lead_with_calls
                    lead_with_calls = sales.get_lead_with_calls(sample_phone)
                    if lead_with_calls:
                        print(f"   ✅ get_lead_with_calls: {lead_with_calls['total_calls']} calls")
                    else:
                        print("   ❌ get_lead_with_calls failed")
                else:
                    print("   ❌ get_lead_by_phone failed")
        
        return True
        
    except Exception as e:
        print(f"❌ SalesOperations test failed: {e}")
        return False

def test_create_update_delete():
    """Test CRUD operations"""
    print("\n🔨 Testing CRUD Operations")
    print("=" * 50)
    
    try:
        client = AirtableClient()
        config = Config.get_table_config()
        leads_table = config['leads_table']
        
        # CREATE
        test_data = {
            "name": "Standardized Test Lead",
            "lead_phone_number": "555STANDARD_TEST",
        }
        
        created = client.create(leads_table, test_data)
        if not created:
            print("   ❌ CREATE failed")
            return False
            
        print(f"   ✅ CREATE: {created['id']}")
        record_id = created['id']
        
        # UPDATE (using fields that exist in your schema)
        update_data = {
            "direccion": "123 Standardized Test Street",
            "referencias": f"Updated via standardized test at {datetime.now().strftime('%H:%M:%S')}"
        }
        
        updated = client.update(leads_table, record_id, update_data)
        if updated:
            print(f"   ✅ UPDATE: {updated['fields'].get('direccion', 'N/A')}")
        else:
            print("   ❌ UPDATE failed")
        
        # DELETE (cleanup)
        deleted = client.delete(leads_table, record_id)
        if deleted:
            print(f"   ✅ DELETE: cleaned up test record")
        else:
            print("   ❌ DELETE failed")
            
        return True
        
    except Exception as e:
        print(f"❌ CRUD test failed: {e}")
        return False

def main():
    """Run all standardized tests"""
    print("🚀 Testing Standardized ADK Sales Agent Setup")
    print("=" * 60)
    
    tests = [
        ("Configuration", test_config),
        ("AirtableClient", test_standardized_client),
        ("SalesOperations", test_sales_operations),
        ("CRUD Operations", test_create_update_delete)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 STANDARDIZATION TEST RESULTS")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 ALL TESTS PASSED!")
        print("✅ Your standardized ADK Sales Agent is ready!")
        print("\n💡 You can now import from:")
        print("   from utils import AirtableClient, SalesOperations")
        print("   or")
        print("   from app.airtable_client import AirtableClient, SalesOperations")
    else:
        print("⚠️  Some tests failed - check configuration")

if __name__ == "__main__":
    main() 