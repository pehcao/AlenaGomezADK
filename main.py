#!/usr/bin/env python3
"""
ADK Sales Agent - Main Application
A telemarketing agent that contacts leads via WhatsApp and handles phone calls
"""

import os
import requests
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

# Load environment variables
load_dotenv()

# Validate required environment variables
required_env_vars = ["OPENAI_API_KEY", "AIRTABLE_API_KEY", "ELEVENLABS_API_KEY"]
for var in required_env_vars:
    if not os.environ.get(var):
        raise ValueError(f"{var} is not set. Please check your .env file.")


@function_tool
def send_whatsapp_template(lead_name: str, lead_number: str):
    """
    Send a WhatsApp template message to a lead
    
    Args:
        lead_name (str): Name of the lead
        lead_number (str): WhatsApp number of the lead
    """
    print(f"Sending WhatsApp message to {lead_name} at {lead_number}")
    
    url = "https://graph.facebook.com/v22.0/648907658307369/messages"
    headers = {
        "Authorization": "Bearer EAAKB8KoOrfcBO6XnkwFqdBMZCGbWZAH4eJS96ZCIPX56k1EbDl6DWEo4oZB7mLNLJTBCIc3NReMEWJozriwoGnh0mUvPZBdnstRlYg4w0VI7mZB77GWKMLHAmFveYZAxspVoU2o2iexBmoWlRYRroEYjfWZCBtJ4R5G2OZBmmrmqlSQsNYNhWx8i5X2NaPdLL3BF5iAoM61WefhwK5ckwjGWLk1iQ",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": lead_number,
        "type": "template",
        "template": {
            "name": "artio_opener",
            "language": {
                "code": "es_MX"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": lead_name
                        },
                    ]
                }
            ]
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Response Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            return f"Successfully sent WhatsApp message to {lead_name}"
        else:
            return f"Failed to send WhatsApp message. Status: {response.status_code}"
            
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        return f"Error sending message: {str(e)}"


def create_sales_agent():
    """Create and configure the sales agent"""
    agent = Agent(
        name="ADK Sales Agent",
        instructions="""You are a helpful telemarketing agent. You receive lead name and number 
        and then contact them via WhatsApp first and then call them via phone once they agree to a call.
        Be professional, friendly, and respectful. Always ask for consent before making phone calls.""",
        tools=[send_whatsapp_template]
    )
    return agent


async def process_lead(lead_info: str):
    """
    Process a lead by sending initial WhatsApp message
    
    Args:
        lead_info (str): Lead information in format "lead name: Name, lead number: Number"
    """
    agent = create_sales_agent()
    result = await Runner.run(agent, lead_info)
    return result.final_output


def main():
    """Main function to run the sales agent"""
    print("ADK Sales Agent initialized successfully!")
    print("Use process_lead() function to handle leads")
    print("Example: await process_lead('lead name: John Doe, lead number: 1234567890')")


if __name__ == "__main__":
    main() 