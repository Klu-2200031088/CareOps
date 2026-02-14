import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SMTP_USER")
        self.sender_password = os.getenv("SMTP_PASSWORD")
    
    def send_email(self, to_email: str, subject: str, body: str, is_html: bool = True):
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = to_email
            
            if is_html:
                part = MIMEText(body, "html")
            else:
                part = MIMEText(body, "plain")
            
            message.attach(part)
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to_email, message.as_string())
            
            return {"status": "sent", "to": to_email}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def send_booking_confirmation(self, contact_email: str, booking_details: dict):
        subject = "Booking Confirmation"
        body = f"""
        <h2>Booking Confirmation</h2>
        <p>Thank you for booking with us!</p>
        <p><strong>Type:</strong> {booking_details.get('booking_type')}</p>
        <p><strong>Date & Time:</strong> {booking_details.get('scheduled_at')}</p>
        <p><strong>Duration:</strong> {booking_details.get('duration_minutes')} minutes</p>
        <p>We look forward to seeing you!</p>
        """
        return self.send_email(contact_email, subject, body)
    
    def send_welcome_message(self, contact_email: str, contact_name: str):
        subject = "Welcome to Our Service"
        body = f"""
        <h2>Welcome {contact_name}!</h2>
        <p>Thank you for reaching out. We'll be in touch shortly.</p>
        <p>Our team will respond to your inquiry within 24 hours.</p>
        """
        return self.send_email(contact_email, subject, body)
    
    def send_form_reminder(self, contact_email: str, form_name: str):
        subject = f"Reminder: {form_name} Pending"
        body = f"""
        <h2>Form Reminder</h2>
        <p>We noticed that <strong>{form_name}</strong> is still pending.</p>
        <p>Please complete it at your earliest convenience.</p>
        """
        return self.send_email(contact_email, subject, body)

# Singleton instance
email_service = EmailService()
