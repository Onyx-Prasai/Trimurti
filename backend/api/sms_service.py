"""
SMS Notification Service for Blood Requests
Uses Twilio to send SMS notifications to nearby donors
"""
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Check if Twilio is configured
try:
    from twilio.rest import Client
    TWILIO_ACCOUNT_SID = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
    TWILIO_AUTH_TOKEN = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
    TWILIO_PHONE_NUMBER = getattr(settings, 'TWILIO_PHONE_NUMBER', None)
    
    if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
        twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        TWILIO_ENABLED = True
    else:
        TWILIO_ENABLED = False
except ImportError:
    TWILIO_ENABLED = False
    logger.warning("Twilio not installed. Install with: pip install twilio")


def send_blood_request_sms(phone_number, blood_type, location, urgency):
    """
    Send SMS notification about blood request to a donor
    
    Args:
        phone_number: Recipient's phone number (with country code e.g., +977XXXXXXXXXX)
        blood_type: Blood type needed (e.g., 'AB+')
        location: Location/district of the request
        urgency: Urgency level (Critical, High, Medium, Low)
    
    Returns:
        bool: True if SMS sent successfully, False otherwise
    """
    if not TWILIO_ENABLED:
        logger.info(f"SMS disabled - would send to {phone_number}: Blood {blood_type} needed in {location} ({urgency})")
        return False
    
    try:
        message = f"🩸 URGENT BLOOD REQUEST 🩸\n\nBlood Type: {blood_type}\nLocation: {location}\nUrgency: {urgency}\n\nYour blood type matches! Please help save lives. Contact the hospital immediately.\n\nReply STOP to unsubscribe."
        
        sms = twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        
        logger.info(f"SMS sent successfully to {phone_number}. SID: {sms.sid}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending SMS to {phone_number}: {str(e)}")
        return False


def send_bulk_blood_request_sms(donors, blood_type, location, urgency):
    """
    Send SMS to multiple donors
    
    Args:
        donors: List of donor objects with phone_number attribute
        blood_type: Blood type needed
        location: Location of the request
        urgency: Urgency level
    
    Returns:
        dict: {success_count, failed_count}
    """
    results = {
        'success_count': 0,
        'failed_count': 0,
        'failed_donors': []
    }
    
    for donor in donors:
        if send_blood_request_sms(donor.phone_number, blood_type, location, urgency):
            results['success_count'] += 1
        else:
            results['failed_count'] += 1
            results['failed_donors'].append(donor.id)
    
    logger.info(f"Bulk SMS results - Success: {results['success_count']}, Failed: {results['failed_count']}")
    return results
