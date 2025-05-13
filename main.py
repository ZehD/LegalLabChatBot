from fastapi import FastAPI, Request, Response
from twilio.twiml.messaging_response import MessagingResponse
from google.cloud import dialogflowcx_v3
from google.cloud.dialogflowcx_v3.types import TextInput, QueryInput
import os
from dotenv import load_dotenv
from google.auth import default
import logging
import sys

# Configure logging (remove the duplicate logging configuration)
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

# Dialogflow CX configuration
DIALOGFLOW_PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")
DIALOGFLOW_LOCATION = os.getenv("DIALOGFLOW_LOCATION", "global")
DIALOGFLOW_AGENT_ID = os.getenv("DIALOGFLOW_AGENT_ID")

# Initialize Google Cloud credentials globally
try:
    credentials, project = default()
    session_client = dialogflowcx_v3.SessionsClient(credentials=credentials)
    logger.info(f"Successfully initialized credentials for service account: {credentials.service_account_email}")
except Exception as e:
    logger.error(f"Error initializing credentials: {e}")
    credentials = None
    session_client = None

@app.get("/")
async def root():
    return {"status": "online"}

@app.get("/test-dialogflow")
async def test_dialogflow():
    try:
        # Create a test session ID
        session_id = "test-session-123"

        # Create session path
        agent_path = f"projects/{DIALOGFLOW_PROJECT_ID}/locations/{DIALOGFLOW_LOCATION}/agents/{DIALOGFLOW_AGENT_ID}"
        session_path = f"{agent_path}/sessions/{session_id}"

        # Create text input
        text_input = TextInput(text="Hello")
        query_input = QueryInput(text=text_input, language_code="en-US")

        # Send request to Dialogflow
        logger.info("Sending test request to Dialogflow...")
        logger.info(f"Using session path: {session_path}")

        response = session_client.detect_intent(
            request={"session": session_path, "query_input": query_input}
        )

        # Log the full response
        logger.info(f"Full Dialogflow response: {response}")

        if response.query_result.response_messages:
            reply = response.query_result.response_messages[0].text.text[0]
            return {"status": "success", "reply": reply}
        else:
            return {"status": "no_response", "raw_response": str(response)}

    except Exception as e:
        logger.error(f"Error testing Dialogflow: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/webhook")
async def webhook(request: Request):
    try:
        # Get the incoming message data from Twilio
        form_data = await request.form()
        incoming_msg = form_data.get('Body', '').strip()
        sender_id = form_data.get('From', '')

        logger.info(f"Received message: '{incoming_msg}' from {sender_id}")
        logger.info(f"Project ID: {DIALOGFLOW_PROJECT_ID}")
        logger.info(f"Location: {DIALOGFLOW_LOCATION}")
        logger.info(f"Agent ID: {DIALOGFLOW_AGENT_ID}")

        # Create session path using alternative approach
        agent_path = f"projects/{DIALOGFLOW_PROJECT_ID}/locations/{DIALOGFLOW_LOCATION}/agents/{DIALOGFLOW_AGENT_ID}"
        session_path = f"{agent_path}/sessions/{sender_id}"

        logger.info(f"Using session path: {session_path}")

        # Create text input
        text_input = TextInput(text=incoming_msg)
        query_input = QueryInput(text=text_input, language_code="en-US")

        try:
            # Send request to Dialogflow
            logger.info("Sending request to Dialogflow...")
            response = session_client.detect_intent(
                request={"session": session_path, "query_input": query_input}
            )
            logger.info(f"Dialogflow raw response: {response}")

            # Create Twilio response
            twilio_response = MessagingResponse()

            if response.query_result.response_messages:
                reply = response.query_result.response_messages[0].text.text[0]
                logger.info(f"Got response from Dialogflow: {reply}")
            else:
                reply = "Sorry, I couldn't process your request at this time."
                logger.warning("No response messages from Dialogflow")

            twilio_response.message(reply)
            return Response(content=str(twilio_response), media_type="application/xml")

        except Exception as dialog_error:
            logger.error(f"Dialogflow error: {str(dialog_error)}")
            # Fall back to echo response for debugging
            twilio_response = MessagingResponse()
            twilio_response.message(f"Echo (Dialogflow error): {incoming_msg}")
            return Response(content=str(twilio_response), media_type="application/xml")

    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        twilio_response = MessagingResponse()
        twilio_response.message(f"Error processing request: {str(e)}")
        return Response(content=str(twilio_response), media_type="application/xml")

@app.on_event("startup")
async def startup_event():
    print("="*50)
    print("STARTUP CONFIGURATION")
    print("="*50)
    print(f"Project ID: {DIALOGFLOW_PROJECT_ID}")
    print(f"Location: {DIALOGFLOW_LOCATION}")
    print(f"Agent ID: {DIALOGFLOW_AGENT_ID}")
    if credentials:
        print(f"Service Account: {credentials.service_account_email}")
    else:
        print("WARNING: No credentials loaded!")
    print("="*50)

    # Verify environment variables
    if not all([DIALOGFLOW_PROJECT_ID, DIALOGFLOW_AGENT_ID]):
        logger.error("Missing required environment variables!")
        for var in ['DIALOGFLOW_PROJECT_ID', 'DIALOGFLOW_LOCATION', 'DIALOGFLOW_AGENT_ID']:
            logger.info(f"{var}: {os.getenv(var)}")