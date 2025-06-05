#!/usr/bin/env python3
"""
Test to extract complete Airtable table schemas
This gets ALL fields regardless of whether they contain data
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.airtable_client import AirtableClient
from config.config import Config
from pyairtable import Api

class SchemaExtractor:
    """Extract complete schemas from Airtable tables"""
    
    def __init__(self):
        """Initialize the schema extractor"""
        print("🔍 Initializing Airtable Schema Extractor")
        print("=" * 60)
        
        if not Config.AIRTABLE_API_KEY:
            raise ValueError("AIRTABLE_API_KEY is required")
            
        self.api = Api(Config.AIRTABLE_API_KEY)
        self.base_id = Config.AIRTABLE_BASE_ID
        self.leads_table = Config.AIRTABLE_LEADS_TABLE_ID
        self.calls_table = Config.AIRTABLE_CALLS_TABLE_ID
        
        print(f"📋 Base ID: {self.base_id}")
        print(f"📋 Leads Table: {self.leads_table}")
        print(f"📋 Calls Table: {self.calls_table}")
        print()
    
    def get_table_schema(self, table_id: str, table_name: str):
        """Get complete schema for a specific table"""
        print(f"🔍 Extracting schema for {table_name} ({table_id})")
        print("-" * 40)
        
        try:
            # Get the base schema which includes all tables and fields
            base = self.api.base(self.base_id)
            schema = base.schema()
            
            # Find our specific table in the schema
            table_schema = None
            for table in schema.tables:
                if table.id == table_id:
                    table_schema = table
                    break
            
            if not table_schema:
                print(f"❌ Table {table_id} not found in base schema")
                return None
            
            # Extract detailed field information
            fields_info = []
            
            print(f"📋 Table Name: {table_schema.name}")
            print(f"📋 Table ID: {table_schema.id}")
            print(f"📋 Total Fields: {len(table_schema.fields)}")
            print()
            
            for field in table_schema.fields:
                field_info = {
                    "id": field.id,
                    "name": field.name,
                    "type": field.type,
                    "description": getattr(field, 'description', None),
                }
                
                # Add type-specific options if they exist (convert to dict for JSON serialization)
                if hasattr(field, 'options') and field.options:
                    try:
                        # Convert options to a JSON-serializable format
                        if hasattr(field.options, '__dict__'):
                            field_info["options"] = field.options.__dict__
                        else:
                            field_info["options"] = str(field.options)
                    except Exception:
                        field_info["options"] = str(field.options)
                
                fields_info.append(field_info)
                
                # Print field details
                print(f"   📝 {field.name}")
                print(f"      Type: {field.type}")
                print(f"      ID: {field.id}")
                if hasattr(field, 'description') and field.description:
                    print(f"      Description: {field.description}")
                if hasattr(field, 'options') and field.options:
                    print(f"      Options: {field.options}")
                print()
            
            # Create complete schema object
            complete_schema = {
                "table_name": table_schema.name,
                "table_id": table_schema.id,
                "total_fields": len(table_schema.fields),
                "extracted_at": datetime.now().isoformat(),
                "fields": fields_info
            }
            
            return complete_schema
            
        except Exception as e:
            print(f"❌ Error extracting schema for {table_name}: {e}")
            return None
    
    def compare_with_record_fields(self, table_id: str, schema_fields: list):
        """Compare schema fields with fields visible in actual records"""
        print(f"🔍 Comparing schema vs. record fields for {table_id}")
        print("-" * 40)
        
        try:
            # Get actual records to see which fields have data
            client = AirtableClient()
            records = client.get_all(table_id)
            
            # Collect all field names that appear in records
            record_fields = set()
            for record in records:
                record_fields.update(record['fields'].keys())
            
            # Get field names from schema
            schema_field_names = {field['name'] for field in schema_fields}
            
            # Compare
            print(f"📊 Schema has {len(schema_field_names)} total fields")
            print(f"📊 Records show {len(record_fields)} fields with data")
            
            # Fields in schema but not in records (empty fields)
            empty_fields = schema_field_names - record_fields
            if empty_fields:
                print(f"📝 Fields in schema but empty in records ({len(empty_fields)}):")
                for field in sorted(empty_fields):
                    print(f"   - {field}")
            else:
                print("✅ All schema fields have data in at least one record")
            
            # Fields in records but not in schema (shouldn't happen)
            unexpected_fields = record_fields - schema_field_names
            if unexpected_fields:
                print(f"⚠️  Fields in records but not in schema ({len(unexpected_fields)}):")
                for field in sorted(unexpected_fields):
                    print(f"   - {field}")
            
            print()
            
            return {
                "schema_fields": len(schema_field_names),
                "record_fields": len(record_fields),
                "empty_fields": list(empty_fields),
                "unexpected_fields": list(unexpected_fields)
            }
            
        except Exception as e:
            print(f"❌ Error comparing fields: {e}")
            return None
    
    def make_json_serializable(self, obj):
        """Convert any object to JSON-serializable format"""
        if obj is None:
            return None
        elif isinstance(obj, (str, int, float, bool)):
            return obj
        elif isinstance(obj, (list, tuple)):
            return [self.make_json_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self.make_json_serializable(value) for key, value in obj.items()}
        elif hasattr(obj, '__dict__'):
            # Convert objects with __dict__ to dictionary
            return {key: self.make_json_serializable(value) for key, value in obj.__dict__.items()}
        else:
            # Convert anything else to string
            return str(obj)
    
    def save_schema_to_file(self, schema: dict, filename: str):
        """Save schema to JSON file"""
        try:
            # Make the entire schema JSON-serializable
            json_schema = self.make_json_serializable(schema)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json_schema, f, indent=2, ensure_ascii=False)
            print(f"✅ Schema saved to: {filename}")
            return True
        except Exception as e:
            print(f"❌ Error saving schema to {filename}: {e}")
            return False
    
    def extract_all_schemas(self):
        """Extract schemas for all tables"""
        print("🚀 Starting Complete Schema Extraction")
        print("=" * 60)
        
        results = {}
        
        # Extract schemas for both tables
        tables_to_extract = [
            (self.leads_table, "Leads Table"),
            (self.calls_table, "Calls Table")
        ]
        
        for table_id, table_name in tables_to_extract:
            print()
            schema = self.get_table_schema(table_id, table_name)
            
            if schema:
                # Compare with actual record fields
                comparison = self.compare_with_record_fields(table_id, schema['fields'])
                schema['field_comparison'] = comparison
                
                # Save to file in schemas directory
                filename = f"../schemas/schema_{table_name.lower().replace(' ', '_')}.json"
                if self.save_schema_to_file(schema, filename):
                    results[table_name] = {
                        "schema": schema,
                        "filename": filename,
                        "success": True
                    }
                else:
                    results[table_name] = {"success": False}
            else:
                results[table_name] = {"success": False}
        
        return results
    
    def create_combined_schema(self, results: dict):
        """Create a combined schema file with both tables"""
        print("\n📄 Creating Combined Schema File")
        print("-" * 40)
        
        combined = {
            "base_id": self.base_id,
            "extracted_at": datetime.now().isoformat(),
            "tables": {}
        }
        
        for table_name, result in results.items():
            if result.get("success") and "schema" in result:
                combined["tables"][table_name] = result["schema"]
        
        filename = "../schemas/complete_airtable_schema.json"
        if self.save_schema_to_file(combined, filename):
            print(f"✅ Combined schema saved to: {filename}")
            return filename
        else:
            return None


def main():
    """Run the schema extraction test"""
    try:
        extractor = SchemaExtractor()
        
        # Extract all schemas
        results = extractor.extract_all_schemas()
        
        # Create combined schema
        combined_file = extractor.create_combined_schema(results)
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 SCHEMA EXTRACTION SUMMARY")
        print("=" * 60)
        
        for table_name, result in results.items():
            if result.get("success"):
                schema = result["schema"]
                print(f"✅ {table_name}:")
                print(f"   📁 File: {result['filename']}")
                print(f"   📝 Fields: {schema['total_fields']}")
                if schema.get('field_comparison'):
                    comp = schema['field_comparison']
                    print(f"   📊 Fields with data: {comp['record_fields']}")
                    print(f"   📊 Empty fields: {len(comp['empty_fields'])}")
            else:
                print(f"❌ {table_name}: Failed to extract")
        
        if combined_file:
            print(f"\n📦 Combined schema: {combined_file}")
        
        print("\n🎉 Schema extraction complete!")
        print("You now have complete field definitions for both tables.")
        
    except Exception as e:
        print(f"❌ Schema extraction failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 