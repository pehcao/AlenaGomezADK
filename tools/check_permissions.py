#!/usr/bin/env python3
"""
Check Airtable API permissions and token type
"""

import os
import sys
from dotenv import load_dotenv

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.airtable_client import AirtableClient

# Load environment variables
load_dotenv()

def check_permissions():
    """Check what permissions the current API token has"""
    
    print("🔐 Checking Airtable API Permissions")
    print("=" * 50)
    
    api_key = os.environ.get("AIRTABLE_API_KEY")
    if not api_key:
        print("❌ No AIRTABLE_API_KEY found")
        return
    
    # Check token type
    print("🔍 API Token Analysis:")
    if api_key.startswith("pat"):
        print("   ✅ Personal Access Token (PAT) detected")
        print("   📝 This is the newer, recommended token type")
    elif api_key.startswith("key"):
        print("   ⚠️  Legacy API Key detected")
        print("   📝 This is the older token type")
    else:
        print("   ❓ Unknown token format")
    
    print(f"   📝 Token starts with: {api_key[:10]}...")
    
    # Test read permissions
    print("\n🔍 Testing READ permissions:")
    client = AirtableClient()
    leads_table = os.environ.get("AIRTABLE_TABLE_ID", "tblUZkxzC0MbJ12HG")
    
    try:
        leads = client.get_all(leads_table)
        if leads:
            print(f"   ✅ READ: Success - found {len(leads)} records")
        else:
            print("   ⚠️  READ: No records found (but no error)")
    except Exception as e:
        print(f"   ❌ READ: Failed - {e}")
        return
    
    # Test write permissions with a minimal test
    print("\n🔧 Testing WRITE permissions:")
    try:
        # Try to create a minimal test record
        test_data = {
            "name": "Permission Test - DELETE ME",
            "lead_phone_number": "000PERMISSION_TEST"
        }
        
        created = client.create(leads_table, test_data)
        
        if created:
            print(f"   ✅ CREATE: Success - created record {created['id']}")
            
            # Test update
            try:
                updated = client.update(leads_table, created['id'], {"name": "Permission Test - UPDATED"})
                if updated:
                    print(f"   ✅ UPDATE: Success")
                else:
                    print(f"   ❌ UPDATE: Failed")
            except Exception as e:
                print(f"   ❌ UPDATE: Failed - {e}")
            
            # Clean up - test delete
            try:
                deleted = client.delete(leads_table, created['id'])
                if deleted:
                    print(f"   ✅ DELETE: Success - cleaned up test record")
                else:
                    print(f"   ❌ DELETE: Failed")
            except Exception as e:
                print(f"   ❌ DELETE: Failed - {e}")
                print(f"   ⚠️  Please manually delete record {created['id']}")
        else:
            print("   ❌ CREATE: Failed")
            
    except Exception as e:
        print(f"   ❌ WRITE: Failed - {e}")
        
        # Check for specific permission errors
        if "401" in str(e) or "AUTHENTICATION_REQUIRED" in str(e):
            print("\n🚨 PERMISSION ISSUE DETECTED:")
            print("   Your API token appears to have READ-only permissions")
            print_permission_help()
        elif "403" in str(e) or "FORBIDDEN" in str(e):
            print("\n🚨 ACCESS ISSUE DETECTED:")
            print("   Your token may not have access to this base/table")
            print_permission_help()

def print_permission_help():
    """Print help for fixing permission issues"""
    
    print("\n" + "=" * 50)
    print("🔧 HOW TO FIX PERMISSION ISSUES")
    print("=" * 50)
    
    print("""
📋 For Personal Access Token (PAT) - RECOMMENDED:

1. Go to: https://airtable.com/create/tokens
2. Create a new token with these scopes:
   ✅ data.records:read
   ✅ data.records:write  
   ✅ schema.bases:read

3. Add your specific base to the token
4. Copy the new token to your .env file

📋 For Legacy API Key (if you must use it):

1. Go to: https://airtable.com/account
2. Generate a new API key
3. Make sure your Airtable base has proper sharing settings:
   - Open your base
   - Click "Share" in top right
   - Make sure the base allows API access

📋 Common Issues:

❌ Read-only token: Your token only has read permissions
❌ Wrong base: Your token doesn't have access to this base  
❌ Wrong table: The table ID is incorrect
❌ Expired token: Your token may have expired

📋 Quick Test:

Try creating a Personal Access Token with full permissions:
- Go to https://airtable.com/create/tokens
- Give it all permissions for testing
- Add your base to the token
- Update your .env file
""")

if __name__ == "__main__":
    check_permissions() 