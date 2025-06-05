#!/usr/bin/env python3
"""
Create a sample lead using the first half of fields from schema_leads_table.json

This script demonstrates how to create a new lead record with proper field types
and data validation based on the extracted Airtable schema.

Based on schema_leads_table.json - using first 18 fields out of 35 total fields.
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.airtable_client import AirtableClient, SalesOperations
from config.config import Config

# Load environment variables
load_dotenv()

def create_sample_lead():
    """Create a sample lead using first half of schema fields"""
    
    print("🆕 Creating Sample Lead - First Half of Schema Fields")
    print("=" * 60)
    
    try:
        # Initialize client
        client = AirtableClient()
        config = Config.get_table_config()
        leads_table = config['leads_table']
        
        print(f"📋 Target table: {leads_table}")
        print()
        
        # FIRST HALF OF SCHEMA FIELDS (18 out of 35 fields)
        # Based on schema_leads_table.json field order
        
        lead_data = {
            # 1. lead_phone_number (singleLineText) - REQUIRED
            "lead_phone_number": "555-DEMO-2024",
            
            # 2. folio (number with precision 0)
            "folio": 12345,
            
            # 3. name (singleLineText) - REQUIRED
            "name": "María González Demo",
            
            # 4. alcaldia (singleLineText) - Location/Municipality
            "alcaldia": "Benito Juárez",
            
            # 5. direccion (multilineText) - Address
            "direccion": "Av. Insurgentes Sur 1234\nCol. Del Valle\nCP 03100",
            
            # 6. referencias (multilineText) - Address references
            "referencias": "Edificio azul, segundo piso\nFrente al parque\nPortón negro",
            
            # 7. lugar_de_prospeccion (singleLineText) - Prospecting location
            "lugar_de_prospeccion": "Feria de Salud CDMX",
            
            # 8. cuantas_persons (number with precision 0) - Number of people
            "cuantas_persons": 4,
            
            # 9. actores (multilineText) - Key people/actors
            "actores": "María González (decisora principal)\nCarlos González (esposo)\nAbuela Carmen (vive con ellos)",
            
            # 10. fecha_follow_up (dateTime) - Follow-up date
            "fecha_follow_up": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d %H:%M"),
            
            # 11. num_llamadas (number with precision 2) - Number of calls
            "num_llamadas": 0.0,
            
            # 12. contactado (singleLineText) - Contact status
            "contactado": "Pendiente",
            
            # 13. last_whatsapp_reachout_datetime (dateTime) - Last WhatsApp contact
            "last_whatsapp_reachout_datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
            
            # 14. num_llamadas_incompletas (number with precision 2) - Incomplete calls
            "num_llamadas_incompletas": 0.0,
            
            # 15. llamada_completa (singleLineText) - Complete call status
            "llamada_completa": "No",
            
            # 16. fecha_cita (dateTime) - Appointment date
            "fecha_cita": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d %H:%M"),
            
            # 17. status (singleLineText) - Current status
            "status": "Nuevo Lead",
            
            # 18. regalo (singleLineText) - Gift/incentive
            "regalo": "Consulta nutricional gratuita"
        }
        
        print("📝 Lead data to be created:")
        print("-" * 40)
        for field, value in lead_data.items():
            field_type = get_field_type(field)
            print(f"   {field:<30} ({field_type:<15}): {value}")
        
        print()
        print("🚀 Creating lead record...")
        
        # Create the lead
        created_lead = client.create(leads_table, lead_data)
        
        if created_lead:
            print(f"✅ Lead created successfully!")
            print(f"📋 Record ID: {created_lead['id']}")
            print(f"📋 Name: {created_lead['fields']['name']}")
            print(f"📋 Phone: {created_lead['fields']['lead_phone_number']}")
            print(f"📋 Status: {created_lead['fields']['status']}")
            
            # Show what fields were actually saved
            print(f"\n📊 Fields saved ({len(created_lead['fields'])} total):")
            for field_name, field_value in created_lead['fields'].items():
                print(f"   ✅ {field_name}: {field_value}")
            
            return created_lead
        else:
            print("❌ Failed to create lead")
            return None
            
    except Exception as e:
        print(f"❌ Error creating lead: {e}")
        return None

def get_field_type(field_name):
    """Get the field type from our schema knowledge"""
    field_types = {
        "lead_phone_number": "singleLineText",
        "folio": "number",
        "name": "singleLineText", 
        "alcaldia": "singleLineText",
        "direccion": "multilineText",
        "referencias": "multilineText",
        "lugar_de_prospeccion": "singleLineText",
        "cuantas_persons": "number",
        "actores": "multilineText",
        "fecha_follow_up": "dateTime",
        "num_llamadas": "number",
        "contactado": "singleLineText",
        "last_whatsapp_reachout_datetime": "dateTime",
        "num_llamadas_incompletas": "number",
        "llamada_completa": "singleLineText",
        "fecha_cita": "dateTime",
        "status": "singleLineText",
        "regalo": "singleLineText"
    }
    return field_types.get(field_name, "unknown")

def test_with_sales_operations():
    """Test the created lead with SalesOperations"""
    
    print("\n🎯 Testing with SalesOperations")
    print("=" * 40)
    
    try:
        # Initialize SalesOperations
        client = AirtableClient()
        config = Config.get_table_config()
        sales = SalesOperations(
            client,
            config['leads_table'],
            config['calls_table']
        )
        
        # Try to find our demo lead
        demo_phone = "555-DEMO-2024"
        lead = sales.get_lead_by_phone(demo_phone)
        
        if lead:
            print(f"✅ Found lead: {lead['fields']['name']}")
            print(f"📞 Phone: {lead['fields']['lead_phone_number']}")
            print(f"📍 Location: {lead['fields']['alcaldia']}")
            print(f"👥 People: {lead['fields']['cuantas_persons']}")
            
            # Get lead with calls
            lead_with_calls = sales.get_lead_with_calls(demo_phone)
            if lead_with_calls:
                print(f"📞 Total calls: {lead_with_calls['total_calls']}")
            
            return lead
        else:
            print("❌ Demo lead not found")
            return None
            
    except Exception as e:
        print(f"❌ Error testing with SalesOperations: {e}")
        return None

def cleanup_demo_lead():
    """Clean up the demo lead (optional)"""
    
    print("\n🧹 Cleanup Demo Lead")
    print("=" * 40)
    
    try:
        client = AirtableClient()
        config = Config.get_table_config()
        
        # Find the demo lead
        demo_phone = "555-DEMO-2024"
        demo_lead = client.find_first(config['leads_table'], "lead_phone_number", demo_phone)
        
        if demo_lead:
            choice = input(f"Found demo lead '{demo_lead['fields']['name']}'. Delete it? (y/n): ")
            if choice.lower() == 'y':
                deleted = client.delete(config['leads_table'], demo_lead['id'])
                if deleted:
                    print("✅ Demo lead deleted successfully")
                else:
                    print("❌ Failed to delete demo lead")
            else:
                print("🔄 Demo lead kept in database")
        else:
            print("ℹ️  No demo lead found to cleanup")
            
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")

def main():
    """Main execution function"""
    
    print("🚀 ADK Sales Agent - Sample Lead Creation")
    print("=" * 60)
    print("Using first 18 fields from schema_leads_table.json")
    print()
    
    # Validate configuration
    try:
        Config.validate_required_env_vars()
        print("✅ Configuration validated")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return
    
    # Create the sample lead
    created_lead = create_sample_lead()
    
    if created_lead:
        # Test with SalesOperations
        test_with_sales_operations()
        
        # Ask about cleanup
        print()
        cleanup_demo_lead()
        
        print("\n🎉 Sample lead creation completed!")
        print("\n💡 Key learnings:")
        print("   ✅ Used 18 out of 35 available fields")
        print("   ✅ Demonstrated proper data types (text, number, dateTime)")
        print("   ✅ Used multilineText for complex data (address, references)")
        print("   ✅ Set realistic business data (folio, status, follow-up dates)")
        print("   ✅ Integrated with SalesOperations layer")
        
    else:
        print("\n❌ Sample lead creation failed")

if __name__ == "__main__":
    main() 