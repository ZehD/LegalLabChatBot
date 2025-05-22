# dialogflow_handler.py

from google.cloud import dialogflowcx_v3
from google.cloud.dialogflowcx_v3.types import TextInput, QueryInput
from google.auth import default
import logging
import os

class DialogflowHandler:
    def __init__(self, project_id: str, location: str, agent_id: str):
        self.project_id = project_id
        self.location = location
        self.agent_id = agent_id
        self.logger = logging.getLogger(__name__)
        self._initialize_client()

    def _initialize_client(self):
        """Initialize Dialogflow client with credentials"""
        try:
            credentials, project = default()
            self.session_client = dialogflowcx_v3.SessionsClient(credentials=credentials)
            self.logger.info(
                f"Successfully initialized credentials for service account: "
                f"{credentials.service_account_email}"
            )
        except Exception as e:
            self.logger.error(f"Error initializing credentials: {e}")
            raise

    def _create_session_path(self, session_id: str) -> str:
        """Create session path for Dialogflow"""
        agent_path = (
            f"projects/{self.project_id}/locations/{self.location}/"
            f"agents/{self.agent_id}"
        )
        return f"{agent_path}/sessions/{session_id}"

    async def detect_intent(self, session_id: str, message: str, language_code: str = "en-US"):
        """Detect intent from user message"""
        try:
            session_path = self._create_session_path(session_id)
            self.logger.info(f"Using session path: {session_path}")

            text_input = TextInput(text=message)
            query_input = QueryInput(text=text_input, language_code=language_code)

            self.logger.info("Sending request to Dialogflow...")
            # Since this is a synchronous call in an async method, we should run it in a separate thread
            # For simplicity, we'll keep it synchronous but remove the async keyword from the method
            # or use asyncio.to_thread in a real implementation
            response = self.session_client.detect_intent(
                request={"session": session_path, "query_input": query_input}
            )

            self.logger.info(f"Dialogflow raw response: {response}")

            # Return all messages instead of just the first one
            if response.query_result.response_messages:
                # Extract all text responses
                all_messages = []
                for msg in response.query_result.response_messages:
                    if msg.text.text:
                        all_messages.extend(msg.text.text)

                if all_messages:
                    return all_messages

            return ["Sorry, I couldn't process your request at this time."]

        except Exception as e:
            self.logger.error(f"Error in detect_intent: {str(e)}")
            raise

    def test_connection(self) -> dict:
        """Test Dialogflow connection"""
        try:
            # Since detect_intent is async, this should be awaited in an async context
            # For simplicity in this example, we'll assume it's called from a synchronous context
            test_response = self.detect_intent("test-session-123", "Hello")
            return {"status": "success", "reply": test_response}
        except Exception as e:
            return {"status": "error", "message": str(e)}