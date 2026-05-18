import uuid
import logging

logger = logging.getLogger(__name__)

class MobileMoneyGateway:
    """
    Modular gateway for African Mobile Money providers (MTN, Airtel).
    Ready for API integration.
    """
    @staticmethod
    def initiate_collection(amount, phone_number, provider='mtn'):
        """
        Simulates a mobile money push (USDT/Momo) to a student's phone.
        """
        logger.info(f"Initiating {provider.upper()} collection of {amount} from {phone_number}")
        
        # Mocking an external API call
        external_id = str(uuid.uuid4())
        
        return {
            "status": "pending",
            "transaction_id": external_id,
            "provider": provider,
            "message": f"Please approve the prompt on your phone ({phone_number})"
        }

    @staticmethod
    def check_status(transaction_id):
        """
        Checks the status of a pending transaction via webhook or polling.
        """
        # Logic to call provider API
        return "SUCCESS"
