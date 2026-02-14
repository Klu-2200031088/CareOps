import os
from typing import Optional, Dict
import requests

class SMSService:
    """
    Twilio SMS Service for sending SMS messages
    """
    
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("TWILIO_PHONE_NUMBER")
        self.api_url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json"
        self.is_configured = bool(self.account_sid and self.auth_token and self.from_number)
    
    def send_sms(self, to_phone: str, message: str) -> Dict:
        """
        Send SMS message via Twilio
        
        Args:
            to_phone: Recipient phone number (e.g., +1234567890)
            message: SMS message content
        
        Returns:
            Dict with status and message ID or error
        """
        if not self.is_configured:
            return {
                "status": "skipped",
                "message": "SMS not configured. Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER"
            }
        
        try:
            auth = (self.account_sid, self.auth_token)
            data = {
                "From": self.from_number,
                "To": to_phone,
                "Body": message
            }
            
            response = requests.post(self.api_url, data=data, auth=auth)
            
            if response.status_code in [200, 201]:
                result = response.json()
                return {
                    "status": "sent",
                    "message_sid": result.get("sid"),
                    "to": to_phone
                }
            else:
                return {
                    "status": "failed",
                    "error": response.json().get("message", "Unknown error"),
                    "code": response.status_code
                }
        
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def send_verification_code(self, phone: str, code: str) -> Dict:
        """
        Send SMS verification code
        
        Args:
            phone: Recipient phone number
            code: 6-digit verification code
        
        Returns:
            Status dict
        """
        message = f"🎯 CareOps Verification Code: {code}\n\nThis code expires in 10 minutes."
        return self.send_sms(phone, message)
    
    def send_booking_reminder(self, phone: str, booking_details: Dict) -> Dict:
        """
        Send booking reminder SMS
        
        Args:
            phone: Recipient phone number
            booking_details: Dict with booking_type, scheduled_at
        
        Returns:
            Status dict
        """
        message = f"📅 Reminder: {booking_details.get('booking_type')} scheduled at {booking_details.get('scheduled_at')}\n\nReply CONFIRM to confirm or CANCEL to cancel."
        return self.send_sms(phone, message)
    
    def send_booking_confirmation(self, phone: str, booking_details: Dict) -> Dict:
        """
        Send booking confirmation SMS
        
        Args:
            phone: Recipient phone number
            booking_details: Dict with booking_type, scheduled_at, confirmation_code
        
        Returns:
            Status dict
        """
        message = f"✅ Booking Confirmed!\n\n📋 Type: {booking_details.get('booking_type')}\n⏰ Time: {booking_details.get('scheduled_at')}\n\nConfirmation: {booking_details.get('confirmation_code', 'N/A')}"
        return self.send_sms(phone, message)
    
    def send_form_reminder(self, phone: str, form_name: str) -> Dict:
        """
        Send form completion reminder
        
        Args:
            phone: Recipient phone number
            form_name: Name of the form to complete
        
        Returns:
            Status dict
        """
        message = f"📋 Reminder: {form_name} is pending.\n\nPlease complete it at your earliest convenience."
        return self.send_sms(phone, message)
    
    def send_inventory_alert(self, phone: str, item_name: str, quantity: int) -> Dict:
        """
        Send low inventory alert
        
        Args:
            phone: Admin phone number
            item_name: Name of inventory item
            quantity: Current quantity
        
        Returns:
            Status dict
        """
        message = f"⚠️ Low Stock Alert\n\n{item_name}: {quantity} units remaining"
        return self.send_sms(phone, message)


# Singleton instance
sms_service = SMSService()
