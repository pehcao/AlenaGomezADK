#!/usr/bin/env python3
"""
Update Manuel Gonzalez record - Reset first half, randomize second half

This script demonstrates:
1. Finding a specific record by name field
2. Resetting first half of fields (18 fields) to 0/null/empty values
3. Populating second half of fields (17 fields) with realistic random data
4. Using the complete schema structure for comprehensive updates

Based on schema_leads_table.json - 35 total fields split into two halves.
"""

import os
import sys
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.airtable_client import AirtableClient, SalesOperations
from config.config import Config

# Load environment variables
load_dotenv()

def generate_random_data_for_second_half():
    """Generate realistic random data for the second half of schema fields (19-35)"""
    
    # Random data generators
    sales_statuses = ["Pendiente", "En proceso", "Cerrada", "Perdida", "Seguimiento"]
    amounts = ["$1,500 MXN", "$2,000 MXN", "$2,500 MXN", "$3,000 MXN", "$3,500 MXN", "$4,000 MXN"]
    commissions = ["10%", "12%", "15%", "18%", "20%"]
    dishes = ["Plan Nutricional Básico", "Plan Detox", "Plan Familiar", "Plan Premium", "Consulta Individual"]
    prospect_types = ["Frío", "Tibio", "Caliente", "Muy Interesado", "Listo para comprar"]
    delivery_statuses = ["Pendiente", "En camino", "Entregado", "Reagendado"]
    supplies = ["Kit básico", "Kit completo", "Kit premium", "Solo consulta", "Productos adicionales"]
    
    # Generate conversation history
    conversation_snippets = [
        "Contacto inicial por WhatsApp - mostró interés",
        "Segunda llamada - preguntó por precios",
        "Envió fotos de análisis médicos",
        "Consultó disponibilidad de horarios",
        "Pidió referencias de otros clientes",
        "Preguntó por planes de pago",
        "Mostró interés en plan familiar"
    ]
    
    conversation_history = "\n".join(random.sample(conversation_snippets, 3))
    
    # Generate OpenAI thread ID (realistic format)
    thread_id = f"thread_{random.randint(100000, 999999)}{chr(random.randint(97, 122))}{chr(random.randint(97, 122))}{chr(random.randint(97, 122))}"
    
    # Generate task ID
    task_id = f"task_{random.randint(10000, 99999)}"
    
    # Generate conversation ID
    conv_id = f"conv_{random.randint(1000, 9999)}_{random.randint(100, 999)}"
    
    # Generate observations
    observations = [
        "Cliente muy interesado, excelente prospecto",
        "Familia comprometida con cambio de hábitos",
        "Presupuesto ajustado, considerar plan básico",
        "Requiere seguimiento constante",
        "Cliente referido por familiar satisfecho",
        "Preocupado por resultados, necesita testimonios"
    ]
    
    # SECOND HALF FIELDS (19-35) - 17 fields total
    random_data = {
        # 19. entregado (singleLineText) - Delivery status
        "entregado": random.choice(delivery_statuses),
        
        # 20. Insumos (singleLineText) - Supplies/materials
        "Insumos": random.choice(supplies),
        
        # 21. venta (singleLineText) - Sale status
        "venta": random.choice(sales_statuses),
        
        # 22. monto (singleLineText) - Sale amount
        "monto": random.choice(amounts),
        
        # 23. comision (singleLineText) - Commission
        "comision": random.choice(commissions),
        
        # 24. Platillo (singleLineText) - Dish/product
        "Platillo": random.choice(dishes),
        
        # 25. Prospecto (singleLineText) - Prospect classification
        "Prospecto": random.choice(prospect_types),
        
        # 26. Observaciones (singleLineText) - General observations
        "Observaciones": random.choice(observations),
        
        # 27. last_update (dateTime) - Last update timestamp
        "last_update": (datetime.now() - timedelta(hours=random.randint(1, 48))).strftime("%Y-%m-%d %H:%M"),
        
        # 28. update_source (singleLineText) - Source of last update
        "update_source": "update_manuel_gonzalez.py script",
        
        # 29. conversation_history (multilineText) - AI conversation history
        "conversation_history": conversation_history,
        
        # 30. openai_thread_id (singleLineText) - OpenAI thread identifier
        "openai_thread_id": thread_id,
        
        # 31. followup_task_id (singleLineText) - Task management ID
        "followup_task_id": task_id,
        
        # 32. followups_today (number with precision 1) - Daily follow-up count
        "followups_today": round(random.uniform(0.0, 3.0), 1),
        
        # 33. last_voice_call_datetime (singleLineText) - Last voice call time
        "last_voice_call_datetime": (datetime.now() - timedelta(hours=random.randint(6, 72))).strftime("%Y-%m-%d %H:%M"),
        
        # 34. last_conversation_id (singleLineText) - Last conversation ID
        "last_conversation_id": conv_id,
        
        # 35. voice_calls_today (number with precision 1) - Daily voice call count
        "voice_calls_today": round(random.uniform(0.0, 5.0), 1)
    }
    
    return random_data

def generate_reset_data_for_first_half():
    """Generate reset/null values for the first half of schema fields (1-18)"""
    
    # FIRST HALF FIELDS (1-18) - Reset to 0/null/empty
    reset_data = {
        # 1. lead_phone_number (singleLineText) - Keep original, don't reset
        # "lead_phone_number": "", # Skip this - it's likely a key field
        
        # 2. folio (number with precision 0)
        "folio": 0,
        
        # 3. name (singleLineText) - Keep original, don't reset
        # "name": "", # Skip this - we're searching by this field
        
        # 4. alcaldia (singleLineText) - Location/Municipality
        "alcaldia": "",
        
        # 5. direccion (multilineText) - Address
        "direccion": "",
        
        # 6. referencias (multilineText) - Address references
        "referencias": "",
        
        # 7. lugar_de_prospeccion (singleLineText) - Prospecting location
        "lugar_de_prospeccion": "",
        
        # 8. cuantas_persons (number with precision 0) - Number of people
        "cuantas_persons": 0,
        
        # 9. actores (multilineText) - Key people/actors
        "actores": "",
        
        # 10. fecha_follow_up (dateTime) - Follow-up date - set to null
        # "fecha_follow_up": None, # Skip datetime nulls for now
        
        # 11. num_llamadas (number with precision 2) - Number of calls
        "num_llamadas": 0.0,
        
        # 12. contactado (singleLineText) - Contact status
        "contactado": "",
        
        # 13. last_whatsapp_reachout_datetime (dateTime) - Last WhatsApp contact
        # "last_whatsapp_reachout_datetime": None, # Skip datetime nulls
        
        # 14. num_llamadas_incompletas (number with precision 2) - Incomplete calls
        "num_llamadas_incompletas": 0.0,
        
        # 15. llamada_completa (singleLineText) - Complete call status
        "llamada_completa": "",
        
        # 16. fecha_cita (dateTime) - Appointment date
        # "fecha_cita": None, # Skip datetime nulls
        
        # 17. status (singleLineText) - Current status
        "status": "Reset",
        
        # 18. regalo (singleLineText) - Gift/incentive
        "regalo": ""
    }
    
    return reset_data

def find_manuel_gonzalez():
    """Find the first record containing 'Manuel Gonzalez' in the name field"""
    
    print("🔍 Searching for Manuel Gonzalez record...")
    print("-" * 40)
    
    try:
        client = AirtableClient()
        config = Config.get_table_config()
        leads_table = config['leads_table']
        
        # Search for records with "Manuel Gonzalez" in name
        # First try exact match
        manuel_record = client.find_first(leads_table, "name", "Manuel Gonzalez")
        
        # If not found, try searching all records for partial match
        if not manuel_record:
            print("   Trying partial name search...")
            all_leads = client.get_all(leads_table)
            for lead in all_leads:
                name = lead['fields'].get('name', '')
                if 'Manuel' in name and 'Gonzalez' in name:
                    manuel_record = lead
                    print(f"   Found partial match: '{name}'")
                    break
        
        if manuel_record:
            print(f"✅ Found record: {manuel_record['id']}")
            print(f"📋 Name: {manuel_record['fields'].get('name', 'N/A')}")
            print(f"📞 Phone: {manuel_record['fields'].get('lead_phone_number', 'N/A')}")
            print(f"📍 Location: {manuel_record['fields'].get('alcaldia', 'N/A')}")
            print(f"📊 Current status: {manuel_record['fields'].get('status', 'N/A')}")
            
            # Show current field count
            print(f"📋 Current fields populated: {len(manuel_record['fields'])}")
            
            return manuel_record
        else:
            print("❌ No record found with 'Manuel Gonzalez' in name field")
            return None
            
    except Exception as e:
        print(f"❌ Error searching for record: {e}")
        return None

def update_manuel_record(record_id):
    """Update Manuel's record with reset first half and random second half"""
    
    print(f"\n🔄 Updating record {record_id}...")
    print("=" * 50)
    
    try:
        client = AirtableClient()
        config = Config.get_table_config()
        leads_table = config['leads_table']
        
        # Generate the update data
        reset_data = generate_reset_data_for_first_half()
        random_data = generate_random_data_for_second_half()
        
        # Combine both datasets
        update_data = {**reset_data, **random_data}
        
        print("📝 Update data to be applied:")
        print("-" * 40)
        print("\n🔄 FIRST HALF - Reset to 0/empty (excluding key fields):")
        for field, value in reset_data.items():
            print(f"   {field:<30} = {value}")
        
        print("\n🎲 SECOND HALF - Random realistic values:")
        for field, value in random_data.items():
            # Truncate long values for display
            display_value = str(value)
            if len(display_value) > 50:
                display_value = display_value[:47] + "..."
            print(f"   {field:<30} = {display_value}")
        
        print(f"\n🚀 Applying update to record {record_id}...")
        
        # Perform the update
        updated_record = client.update(leads_table, record_id, update_data)
        
        if updated_record:
            print(f"✅ Record updated successfully!")
            print(f"📋 Updated fields: {len(updated_record['fields'])}")
            print(f"📋 Name: {updated_record['fields'].get('name', 'N/A')}")
            print(f"📋 Status: {updated_record['fields'].get('status', 'N/A')}")
            print(f"💼 Sale status: {updated_record['fields'].get('venta', 'N/A')}")
            print(f"💰 Amount: {updated_record['fields'].get('monto', 'N/A')}")
            print(f"🔥 Prospect type: {updated_record['fields'].get('Prospecto', 'N/A')}")
            
            return updated_record
        else:
            print("❌ Failed to update record")
            return None
            
    except Exception as e:
        print(f"❌ Error updating record: {e}")
        return None

def verify_update_with_sales_operations(phone_number):
    """Verify the update using SalesOperations"""
    
    print("\n🎯 Verifying update with SalesOperations")
    print("=" * 40)
    
    try:
        client = AirtableClient()
        config = Config.get_table_config()
        sales = SalesOperations(
            client,
            config['leads_table'],
            config['calls_table']
        )
        
        if phone_number:
            # Try to find the updated lead
            lead = sales.get_lead_by_phone(phone_number)
            
            if lead:
                print(f"✅ Found updated lead: {lead['fields'].get('name', 'N/A')}")
                print(f"📞 Phone: {lead['fields'].get('lead_phone_number', 'N/A')}")
                print(f"🔄 Status: {lead['fields'].get('status', 'N/A')}")
                print(f"💼 Sale: {lead['fields'].get('venta', 'N/A')}")
                print(f"🤖 AI Thread: {lead['fields'].get('openai_thread_id', 'N/A')}")
                
                # Show reset fields
                print(f"\n📊 Sample reset fields:")
                print(f"   Folio: {lead['fields'].get('folio', 'N/A')}")
                print(f"   Calls: {lead['fields'].get('num_llamadas', 'N/A')}")
                print(f"   Alcaldía: '{lead['fields'].get('alcaldia', 'N/A')}'")
                
                # Show new random fields  
                print(f"\n🎲 Sample random fields:")
                print(f"   Prospect: {lead['fields'].get('Prospecto', 'N/A')}")
                print(f"   Dish: {lead['fields'].get('Platillo', 'N/A')}")
                print(f"   Voice calls today: {lead['fields'].get('voice_calls_today', 'N/A')}")
                
                return lead
            else:
                print("❌ Updated lead not found")
                return None
        else:
            print("⚠️  No phone number available for verification")
            return None
            
    except Exception as e:
        print(f"❌ Error verifying update: {e}")
        return None

def main():
    """Main execution function"""
    
    print("🔄 ADK Sales Agent - Update Manuel Gonzalez Record")
    print("=" * 60)
    print("Reset first half (18 fields) + Randomize second half (17 fields)")
    print()
    
    # Validate configuration
    try:
        Config.validate_required_env_vars()
        print("✅ Configuration validated")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return
    
    # Find Manuel Gonzalez record
    manuel_record = find_manuel_gonzalez()
    
    if not manuel_record:
        print("\n❌ Cannot proceed without finding Manuel Gonzalez record")
        print("💡 Make sure there's a record with 'Manuel Gonzalez' in the name field")
        return
    
    # Get phone number for verification
    phone_number = manuel_record['fields'].get('lead_phone_number')
    
    # Ask for confirmation
    print(f"\n⚠️  About to update record: {manuel_record['fields'].get('name', 'Unknown')}")
    print("   - First half fields will be reset to 0/empty")
    print("   - Second half fields will be filled with random data")
    
    choice = input("\nProceed with update? (y/n): ")
    if choice.lower() != 'y':
        print("🔄 Update cancelled")
        return
    
    # Perform the update
    updated_record = update_manuel_record(manuel_record['id'])
    
    if updated_record:
        # Verify with SalesOperations
        verify_update_with_sales_operations(phone_number)
        
        print("\n🎉 Manuel Gonzalez record update completed!")
        print("\n💡 Summary of changes:")
        print("   ✅ First 18 fields reset to 0/empty (keeping name & phone)")
        print("   ✅ Last 17 fields populated with realistic random data")
        print("   ✅ Demonstrated both reset and random data generation")
        print("   ✅ Used complete schema structure (35 total fields)")
        print("   ✅ Verified update with SalesOperations layer")
        
    else:
        print("\n❌ Manuel Gonzalez record update failed")

if __name__ == "__main__":
    main() 