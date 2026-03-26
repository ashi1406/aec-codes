# backend/app/services/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional
import logging
from pathlib import Path
from jinja2 import Template
from datetime import datetime

from app.config import settings
from app.models import Event, Participant

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.username = settings.SMTP_USERNAME
        self.password = settings.SMTP_PASSWORD
        
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        attachments: Optional[List[Path]] = None
    ) -> bool:
        """Send email with HTML content"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Attach HTML content
            msg.attach(MIMEText(html_content, 'html'))
            
            # Attach files
            if attachments:
                for file_path in attachments:
                    with open(file_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename={file_path.name}'
                        )
                        msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    def send_venue_booking_notification(
        self,
        event: Event,
        venue_name: str,
        start_time: datetime,
        end_time: datetime
    ):
        """Send venue booking notification to maintenance"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #1976d2; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .details {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; }}
                .footer {{ text-align: center; padding: 20px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>🔔 Venue Booking Confirmation</h2>
                </div>
                <div class="content">
                    <p>Dear Maintenance Team,</p>
                    <p>A new venue has been booked for the following event:</p>
                    
                    <div class="details">
                        <h3>Event Details</h3>
                        <p><strong>Event:</strong> {event.name}</p>
                        <p><strong>Venue:</strong> {venue_name}</p>
                        <p><strong>Start:</strong> {start_time.strftime('%B %d, %Y at %I:%M %p')}</p>
                        <p><strong>End:</strong> {end_time.strftime('%B %d, %Y at %I:%M %p')}</p>
                        <p><strong>Coordinator:</strong> {event.coordinator}</p>
                        <p><strong>Expected Participants:</strong> {event.max_participants}</p>
                    </div>
                    
                    <p>Please ensure the venue is prepared and all necessary equipment is functional.</p>
                    
                    <h4>Requirements:</h4>
                    <ul>
                        <li>Projector setup</li>
                        <li>Sound system check</li>
                        <li>Seating arrangement</li>
                        <li>Water dispensers</li>
                    </ul>
                    
                    <p>Thank you for your support!</p>
                </div>
                <div class="footer">
                    <p>This is an automated message from Event Management System</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(
            to_email=settings.MAINTENANCE_EMAIL,
            subject=f"🔔 Venue Booked: {venue_name} for {event.name}",
            html_content=html
        )
    
    def send_registration_confirmation(self, participant: Participant, event: Event):
        """Send registration confirmation to participant"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4caf50; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .details {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; }}
                .qr-code {{ text-align: center; padding: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>✅ Registration Confirmed!</h2>
                </div>
                <div class="content">
                    <p>Dear {participant.name},</p>
                    <p>Your registration for the following event has been confirmed:</p>
                    
                    <div class="details">
                        <h3>{event.name}</h3>
                        <p><strong>Date:</strong> {event.start_date.strftime('%B %d, %Y')}</p>
                        <p><strong>Time:</strong> {event.start_date.strftime('%I:%M %p')} - {event.end_date.strftime('%I:%M %p')}</p>
                        <p><strong>Venue:</strong> {event.venue.name if event.venue else 'To be announced'}</p>
                    </div>
                    
                    <div class="qr-code">
                        <p><strong>Your QR Code for check-in:</strong></p>
                        <!-- QR code would be generated here -->
                        <div style="width: 150px; height: 150px; background-color: #eee; margin: 0 auto;"></div>
                    </div>
                    
                    <h4>Important Information:</h4>
                    <ul>
                        <li>Please arrive 15 minutes before the event</li>
                        <li>Bring your college ID card</li>
                        <li>Show the QR code at the entrance</li>
                    </ul>
                    
                    <p>We look forward to seeing you at the event!</p>
                </div>
                <div class="footer">
                    <p>Event Management System</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(
            to_email=participant.email,
            subject=f"✅ Registration Confirmed: {event.name}",
            html_content=html
        )
    
    def send_score_notification(self, participant: Participant, event: Event, score: float):
        """Send score update notification"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #ff9800; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .score {{ font-size: 48px; text-align: center; padding: 20px; }}
                .details {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>🏆 Your Score is Ready!</h2>
                </div>
                <div class="content">
                    <p>Dear {participant.name},</p>
                    <p>Your score for <strong>{event.name}</strong> has been published.</p>
                    
                    <div class="score">
                        <strong>{score:.1f}</strong> points
                    </div>
                    
                    <div class="details">
                        <h4>Performance Summary:</h4>
                        <p>You scored {score:.1f} out of 100 in this event.</p>
                        <p>Check the leaderboard to see your ranking!</p>
                    </div>
                    
                    <p>Keep participating in more events to improve your overall score!</p>
                </div>
                <div class="footer">
                    <p>Event Management System</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(
            to_email=participant.email,
            subject=f"🏆 Score Update: {event.name}",
            html_content=html
        )

# Create singleton instance
email_service = EmailService()