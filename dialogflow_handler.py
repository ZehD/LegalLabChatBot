# dialogflow_handler.py

from google.cloud import dialogflowcx_v3
from google.cloud.dialogflowcx_v3.types import TextInput, QueryInput
from google.auth import default
from google.oauth2 import service_account
import logging
import os
import json
import asyncio

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
            # Check if GOOGLE_APPLICATION_CREDENTIALS contains JSON content
            creds_env = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

            if creds_env and creds_env.strip().startswith('{'):
                # It's JSON content, parse it
                self.logger.info("Using JSON credentials from environment variable")
                credentials_info = json.loads(creds_env)
                credentials = service_account.Credentials.from_service_account_info(credentials_info)
                self.session_client = dialogflowcx_v3.SessionsClient(credentials=credentials)
                self.logger.info(f"Successfully initialized credentials for service account: {credentials_info.get('client_email')}")
            else:
                # It's a file path or use default
                self.logger.info("Using default credentials method")
                credentials, project = default()
                self.session_client = dialogflowcx_v3.SessionsClient(credentials=credentials)
                if hasattr(credentials, 'service_account_email'):
                    self.logger.info(f"Successfully initialized credentials for service account: {credentials.service_account_email}")
                else:
                    self.logger.info("Successfully initialized credentials using default method")

        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing JSON credentials: {e}")
            raise
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

    async def test_connection(self):
        """Test Dialogflow connection"""
        try:
            return {
                "status": "connected",
                "project_id": self.project_id,
                "location": self.location,
                "agent_id": self.agent_id
            }
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return {"status": "error", "message": str(e)}

    async def detect_intent(self, session_id: str, message: str, language_code: str = "en-US"):
        """Detect intent from user message"""
        try:
            session_path = self._create_session_path(session_id)
            self.logger.info(f"Using session path: {session_path}")

            text_input = TextInput(text=message)
            query_input = QueryInput(text=text_input, language_code=language_code)

            self.logger.info("Sending request to Dialogflow...")

            # Run the synchronous Dialogflow call in a separate thread
            response = await asyncio.to_thread(
                self.session_client.detect_intent,
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