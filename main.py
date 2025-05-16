# main.py

from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv
import logging
import sys
from dialogflow_handler import DialogflowHandler
from twilio_handler import TwilioHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize handlers
dialogflow_handler = DialogflowHandler(
    project_id=os.getenv("DIALOGFLOW_PROJECT_ID"),
    location=os.getenv("DIALOGFLOW_LOCATION", "global"),
    agent_id=os.getenv("DIALOGFLOW_AGENT_ID")
)
twilio_handler = TwilioHandler()

@app.get("/")
async def root():
    return {"status": "online"}

@app.get("/test-dialogflow")
async def test_dialogflow():
    try:
        return await dialogflow_handler.test_connection()
    except Exception as e:
        logger.error(f"Error testing Dialogflow: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/webhook")
async def webhook(request: Request):
    try:
        # Get form data from request
        form_data = await request.form()

        # Process incoming message using Twilio handler
        message, sender_id = await twilio_handler.process_incoming_message(form_data)

        # Get response from Dialogflow
        dialogflow_response = await dialogflow_handler.detect_intent(
            session_id=sender_id,
            message=message
        )

        # Create and return Twilio response
        return twilio_handler.create_response(dialogflow_response)

    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        return twilio_handler.create_response(f"Error processing request: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Print startup configuration"""
    print("="*50)
    print("STARTUP CONFIGURATION")
    print("="*50)
    print(f"Project ID: {os.getenv('DIALOGFLOW_PROJECT_ID')}")
    print(f"Location: {os.getenv('DIALOGFLOW_LOCATION')}")
    print(f"Agent ID: {os.getenv('DIALOGFLOW_AGENT_ID')}")
    print("="*50)

    # Verify environment variables
    required_vars = ['DIALOGFLOW_PROJECT_ID', 'DIALOGFLOW_AGENT_ID']
    if not all(os.getenv(var) for var in required_vars):
        logger.error("Missing required environment variables!")
        for var in required_vars:
            logger.info(f"{var}: {os.getenv(var)}")