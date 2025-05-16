# twilio_handler.py

from twilio.twiml.messaging_response import MessagingResponse
from fastapi import Response
import logging

class TwilioHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_response(self, message: str) -> Response:
        """Create a Twilio response"""
        try:
            twilio_response = MessagingResponse()
            twilio_response.message(message)
            return Response(
                content=str(twilio_response),
                media_type="application/xml"
            )
        except Exception as e:
            self.logger.error(f"Error creating Twilio response: {e}")
            raise

    async def process_incoming_message(self, form_data: dict) -> tuple:
        """Process incoming message from Twilio"""
        try:
            message = form_data.get('Body', '').strip()
            sender_id = form_data.get('From', '')

            self.logger.info(f"Received message: '{message}' from {sender_id}")

            return message, sender_id
        except Exception as e:
            self.logger.error(f"Error processing incoming message: {e}")
            raise