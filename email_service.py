import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("SMTP_FROM_EMAIL")
        
        if not all([self.smtp_host, self.smtp_username, self.smtp_password, self.from_email]):
            logger.warning("Email service not fully configured")

    def send_email(self, to_emails: List[str], subject: str, body: str, html_body: str = None):
        if not self.smtp_host:
            logger.error("Email service not configured")
            return False

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = ', '.join(to_emails)

            # Add text part
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)

            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {to_emails}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    def send_alert_email(self, to_emails: List[str], alert_type: str, description: str, camera_name: str):
        subject = f"Security Alert: {alert_type}"
        body = f"""
        Security Alert Detected
        
        Type: {alert_type}
        Description: {description}
        Camera: {camera_name}
        Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
        
        Please review the surveillance system immediately.
        """
        
        html_body = f"""
        <html>
        <body>
            <h2 style="color: #dc2626;">Security Alert Detected</h2>
            <p><strong>Type:</strong> {alert_type}</p>
            <p><strong>Description:</strong> {description}</p>
            <p><strong>Camera:</strong> {camera_name}</p>
            <p><strong>Time:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            <p style="color: #dc2626;"><strong>Please review the surveillance system immediately.</strong></p>
        </body>
        </html>
        """
        
        return self.send_email(to_emails, subject, body, html_body)

# Global email service instance
email_service = EmailService()