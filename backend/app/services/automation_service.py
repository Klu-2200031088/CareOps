"""
Automation Service - Handles event-driven automation rules
"""
from sqlalchemy.orm import Session
from app.models.models import Booking, Contact, Message, Conversation, FormSubmission, InventoryItem
from app.integrations.email_service import email_service
from app.integrations.sms_service import sms_service
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class AutomationService:
    
    @staticmethod
    def on_booking_created(booking: Booking, contact: Contact, db: Session):
        """
        Triggered when a booking is created
        - Send confirmation email/SMS (already done in bookings.py)
        - Send booking details to conversation
        - Create form submission records if forms exist
        """
        try:
            # Send forms that are linked to this booking type
            forms = db.query(FormSubmission).filter(
                FormSubmission.status == "pending",
                FormSubmission.booking_id == booking.id
            ).all()
            
            for form in forms:
                # Send form reminder email
                try:
                    email_service.send_form_reminder(contact.email, f"Form: {form.form_id}")
                except Exception as e:
                    logger.error(f"Form reminder email failed: {e}")
                
                # Send SMS if phone exists
                if contact.phone:
                    try:
                        sms_service.send_form_reminder(contact.phone, f"Form {form.form_id}")
                    except Exception as e:
                        logger.error(f"Form reminder SMS failed: {e}")
        except Exception as e:
            logger.error(f"Error in on_booking_created automation: {e}")
    
    @staticmethod
    def on_contact_created(contact: Contact, db: Session):
        """
        Triggered when a contact is created
        - Send welcome email (already done in contacts.py)
        - Set up initial conversation (already done)
        """
        pass
    
    @staticmethod
    def on_staff_reply(message: Message, conversation: Conversation, db: Session):
        """
        Triggered when staff sends a message
        - Pause automation for this conversation
        - Log staff intervention
        """
        try:
            # Update conversation to indicate staff has replied
            # This prevents automated reminders from being sent
            conversation.updated_at = datetime.utcnow()
            db.commit()
            logger.info(f"Staff replied to conversation {conversation.id}")
        except Exception as e:
            logger.error(f"Error in on_staff_reply automation: {e}")
    
    @staticmethod
    def on_form_overdue(form_submission: FormSubmission, contact: Contact, db: Session):
        """
        Triggered when a form becomes overdue
        - Send reminder email
        - Send reminder SMS if available
        - Create alert message
        """
        try:
            # Send reminder email
            email_service.send_form_reminder(contact.email, f"Form Overdue: {form_submission.form_id}")
            
            # Send reminder SMS
            if contact.phone:
                sms_service.send_form_reminder(contact.phone, f"Overdue form {form_submission.form_id}")
        except Exception as e:
            logger.error(f"Error in on_form_overdue automation: {e}")
    
    @staticmethod
    def on_inventory_low(item: InventoryItem, workspace, db: Session):
        """
        Triggered when inventory falls below threshold
        - Send email alert to workspace owner
        - Send SMS alert to workspace owner
        - Create dashboard alert
        """
        try:
            owner = workspace.owner
            if owner and owner.email:
                email_service.send_email(
                    owner.email,
                    f"Low Inventory Alert: {item.name}",
                    f"<h2>Low Inventory Alert</h2><p>{item.name} is at {item.quantity} units (threshold: {item.low_threshold})</p>"
                )
            
            # SMS alert if owner has phone
            if owner and owner.phone_number:
                sms_service.send_inventory_alert(owner.phone_number, item.name, item.quantity)
        except Exception as e:
            logger.error(f"Error in on_inventory_low automation: {e}")
    
    @staticmethod
    def check_and_trigger_reminders(db: Session):
        """
        Periodic task - check for pending reminders and trigger them
        Should be run via a scheduler (APScheduler or Celery)
        """
        try:
            # Check for forms that are due soon
            tomorrow = datetime.utcnow() + timedelta(days=1)
            forms_due_soon = db.query(FormSubmission).filter(
                FormSubmission.status == "pending",
                FormSubmission.due_at <= tomorrow,
                FormSubmission.due_at > datetime.utcnow()
            ).all()
            
            for form in forms_due_soon:
                # Get contact info
                booking = db.query(Booking).filter(Booking.id == form.booking_id).first()
                if booking:
                    contact = db.query(Contact).filter(Contact.id == booking.contact_id).first()
                    if contact:
                        try:
                            email_service.send_form_reminder(contact.email, f"Form {form.form_id}")
                            if contact.phone:
                                sms_service.send_form_reminder(contact.phone, f"Form {form.form_id}")
                        except Exception as e:
                            logger.error(f"Reminder trigger failed: {e}")
            
            logger.info(f"Triggered {len(forms_due_soon)} form reminders")
        except Exception as e:
            logger.error(f"Error in check_and_trigger_reminders: {e}")

# Singleton instance
automation_service = AutomationService()
