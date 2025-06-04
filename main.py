from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv
import logging
import sys
from dialogflow_handler import DialogflowHandler

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
app = FastAPI(title="Legal Chatbot API", version="1.0.0")

# Initialize Dialogflow handler
try:
    dialogflow_handler = DialogflowHandler(
        project_id=os.getenv("DIALOGFLOW_PROJECT_ID"),
        location=os.getenv("DIALOGFLOW_LOCATION", "global"),
        agent_id=os.getenv("DIALOGFLOW_AGENT_ID")
    )
    logger.info("Dialogflow handler initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Dialogflow handler: {e}")
    dialogflow_handler = None

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Legal Chatbot API",
        "version": "1.0.0",
        "dialogflow_ready": dialogflow_handler is not None
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "dialogflow_connection": "ready" if dialogflow_handler else "error"
    }

@app.get("/test-dialogflow")
async def test_dialogflow():
    """Test Dialogflow connection"""
    if not dialogflow_handler:
        return {"status": "error", "message": "Dialogflow handler not initialized"}

    try:
        return await dialogflow_handler.test_connection()
    except Exception as e:
        logger.error(f"Error testing Dialogflow: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/chat")
async def chat_endpoint(request: Request):
    """Simple chat endpoint for local testing"""
    try:
        # Parse JSON request
        data = await request.json()
        message = data.get("message", "").strip()
        session_id = data.get("session_id", "test-session-123")

        if not message:
            return {"error": "Message is required"}

        if not dialogflow_handler:
            return {"error": "Dialogflow not available"}

        logger.info(f"Processing message: '{message}' for session: {session_id}")

        # Get response from Dialogflow
        dialogflow_response = await dialogflow_handler.detect_intent(
            session_id=session_id,
            message=message
        )

        # Format response
        if isinstance(dialogflow_response, list):
            response_text = "\n".join(dialogflow_response)
        else:
            response_text = str(dialogflow_response)

        return {
            "response": response_text,
            "session_id": session_id,
            "status": "success"
        }

    except Exception as e:
        logger.error(f"Chat processing error: {str(e)}")
        return {"error": f"Error processing request: {str(e)}"}

@app.post("/webhook")
async def webhook(request: Request):
    """Webhook endpoint for Dialogflow CX fulfillment"""
    try:
        # Handle Dialogflow CX webhook format
        json_data = await request.json()
        logger.info(f"Received webhook: {json_data}")

        # Extract information from Dialogflow CX format
        text_input = json_data.get("text", "")
        session_info = json_data.get("sessionInfo", {})
        session_id = session_info.get("session", "").split("/")[-1]
        intent_info = json_data.get("intentInfo", {})
        intent_name = intent_info.get("displayName", "")

        logger.info(f"Intent: {intent_name}, Message: {text_input}, Session: {session_id}")

        # Custom logic based on intent
        response_text = await process_custom_logic(text_input, intent_name, session_id)

        # Return Dialogflow CX fulfillment response
        return {
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": [response_text]
                        }
                    }
                ]
            }
        }

    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return {
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": ["Sorry, I'm experiencing technical difficulties."]
                        }
                    }
                ]
            }
        }

async def process_custom_logic(message: str, intent_name: str, session_id: str) -> str:
    """Process custom business logic"""
    try:
        # Example custom responses based on intent
        if "legal" in intent_name.lower() or "help" in intent_name.lower():
            return f"🏛️ I understand you need legal assistance. You mentioned: '{message}'. Let me help you with relevant legal resources."

        elif "document" in intent_name.lower():
            return "📄 I can help with legal documents. What type of document do you need assistance with? (contracts, wills, divorce papers, etc.)"

        elif "emergency" in intent_name.lower():
            return "🚨 This seems urgent. Here are emergency legal contacts:\n• Legal Aid Hotline: 1-800-LEGAL-AID\n• Emergency Court Services: Contact your local courthouse"

        else:
            # Fallback to Dialogflow for other cases
            if dialogflow_handler:
                response = await dialogflow_handler.detect_intent(session_id, message)
                if isinstance(response, list):
                    return "\n".join(response)
                return str(response)
            else:
                return "I'm here to help with legal questions. Could you please be more specific about what you need?"

    except Exception as e:
        logger.error(f"Error in custom logic: {str(e)}")
        return "I'm here to help with your legal questions. Could you please rephrase your request?"

@app.on_event("startup")
async def startup_event():
    """Print startup configuration"""
    print("="*50)
    print("🤖 LEGAL CHATBOT STARTUP")
    print("="*50)
    print(f"Project ID: {os.getenv('DIALOGFLOW_PROJECT_ID')}")
    print(f"Location: {os.getenv('DIALOGFLOW_LOCATION')}")
    print(f"Agent ID: {os.getenv('DIALOGFLOW_AGENT_ID')}")
    print(f"Dialogflow Ready: {dialogflow_handler is not None}")
    print("="*50)
    print("🚀 Available endpoints:")
    print("   GET  /          - Status check")
    print("   GET  /health    - Health check")
    print("   GET  /test-dialogflow - Test Dialogflow connection")
    print("   POST /chat      - Simple chat interface")
    print("   POST /webhook   - Dialogflow CX webhook")
    print("="*50)