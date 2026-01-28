"""
SMS Notification Service for Blood Requests
Supports multiple SMS providers: Sparrow SMS (Nepal) and Twilio (International)
Automatically falls back between providers
"""
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

# ==================== SPARROW SMS (Nepal) Configuration ====================
SPARROW_TOKEN = getattr(settings, 'SPARROW_TOKEN', None)
SPARROW_FROM = getattr(settings, 'SPARROW_FROM', None)
SPARROW_ENABLED = bool(SPARROW_TOKEN and SPARROW_FROM)

# ==================== SMS PASAL (Nepal) Configuration ====================
SMS_PASAL_TOKEN = getattr(settings, 'SMS_PASAL_TOKEN', None)
SMS_PASAL_FROM = getattr(settings, 'SMS_PASAL_FROM', None)
SMS_PASAL_ENABLED = bool(SMS_PASAL_TOKEN and SMS_PASAL_FROM)

# ==================== TWILIO Configuration ====================
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

# Determine which provider to use (prefer Nepal providers first)
SMS_ENABLED = SPARROW_ENABLED or SMS_PASAL_ENABLED or TWILIO_ENABLED
if SPARROW_ENABLED:
    SMS_PROVIDER = 'sparrow'
elif SMS_PASAL_ENABLED:
    SMS_PROVIDER = 'sms_pasal'
elif TWILIO_ENABLED:
    SMS_PROVIDER = 'twilio'
else:
    SMS_PROVIDER = None


def _send_sms_sparrow(phone_number, message):
    """
    Send SMS using Sparrow SMS (Nepal provider)
    
    Args:
        phone_number: Phone number (with or without country code)
        message: Message text
    
    Returns:
        dict: {'success': bool, 'message_sid': str or None, 'error': str or None}
    """
    try:
        # Remove + and country code if present, keep only digits
        phone_clean = phone_number.replace('+', '').replace(' ', '').replace('-', '')
        if phone_clean.startswith('977'):
            phone_clean = phone_clean[3:]  # Remove country code for Nepal
        
        url = "https://api.sparrowsms.com/v2/sms/"
        payload = {
            "token": SPARROW_TOKEN,
            "from": SPARROW_FROM,
            "to": phone_clean,
            "text": message
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('response_code') == 200:
                logger.info(f"Sparrow SMS sent successfully to {phone_number}")
                return {
                    'success': True,
                    'message_sid': str(data.get('id', '')),
                    'error': None,
                    'provider': 'sparrow'
                }
            else:
                error_msg = data.get('response_message', 'Unknown error')
                logger.error(f"Sparrow SMS error: {error_msg}")
                return {
                    'success': False,
                    'message_sid': None,
                    'error': f"Sparrow SMS: {error_msg}",
                    'provider': 'sparrow'
                }
        else:
            error_msg = f"HTTP {response.status_code}: {response.text}"
            logger.error(f"Sparrow SMS HTTP error: {error_msg}")
            return {
                'success': False,
                'message_sid': None,
                'error': f"Sparrow SMS: {error_msg}",
                'provider': 'sparrow'
            }
            
    except requests.exceptions.Timeout:
        error_msg = "Connection timeout to Sparrow SMS API"
        logger.error(f"Sparrow SMS: {error_msg}")
        return {
            'success': False,
            'message_sid': None,
            'error': error_msg,
            'provider': 'sparrow'
        }
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Sparrow SMS error: {error_msg}")
        return {
            'success': False,
            'message_sid': None,
            'error': f"Sparrow SMS: {error_msg}",
            'provider': 'sparrow'
        }


def _send_sms_sms_pasal(phone_number, message):
    """
    Send SMS using SMS Pasal (Nepal provider)
    
    Args:
        phone_number: Phone number (with or without country code)
        message: Message text
    
    Returns:
        dict: {'success': bool, 'message_sid': str or None, 'error': str or None}
    """
    try:
        # Remove + and country code if present, keep only digits
        phone_clean = phone_number.replace('+', '').replace(' ', '').replace('-', '')
        if phone_clean.startswith('977'):
            phone_clean = phone_clean[3:]  # Remove country code for Nepal
        
        # SMS Pasal API endpoint (check their docs for exact endpoint)
        url = "https://api.smspasal.com/send"  # Update with actual endpoint
        payload = {
            "token": SMS_PASAL_TOKEN,
            "from": SMS_PASAL_FROM,
            "to": phone_clean,
            "text": message
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success' or data.get('success'):
                logger.info(f"SMS Pasal SMS sent successfully to {phone_number}")
                return {
                    'success': True,
                    'message_sid': str(data.get('id', data.get('message_id', ''))),
                    'error': None,
                    'provider': 'sms_pasal'
                }
            else:
                error_msg = data.get('message', data.get('error', 'Unknown error'))
                logger.error(f"SMS Pasal error: {error_msg}")
                return {
                    'success': False,
                    'message_sid': None,
                    'error': f"SMS Pasal: {error_msg}",
                    'provider': 'sms_pasal'
                }
        else:
            error_msg = f"HTTP {response.status_code}: {response.text}"
            logger.error(f"SMS Pasal HTTP error: {error_msg}")
            return {
                'success': False,
                'message_sid': None,
                'error': f"SMS Pasal: {error_msg}",
                'provider': 'sms_pasal'
            }
            
    except requests.exceptions.Timeout:
        error_msg = "Connection timeout to SMS Pasal API"
        logger.error(f"SMS Pasal: {error_msg}")
        return {
            'success': False,
            'message_sid': None,
            'error': error_msg,
            'provider': 'sms_pasal'
        }
    except Exception as e:
        error_msg = str(e)
        logger.error(f"SMS Pasal error: {error_msg}")
        return {
            'success': False,
            'message_sid': None,
            'error': f"SMS Pasal: {error_msg}",
            'provider': 'sms_pasal'
        }


def _send_sms_twilio(phone_number, message):
    """
    Send SMS using Twilio
    
    Args:
        phone_number: Phone number (E.164 format)
        message: Message text
    
    Returns:
        dict: {'success': bool, 'message_sid': str or None, 'error': str or None}
    """
    try:
        # Check if trying to send to the same number as Twilio number
        if phone_number == TWILIO_PHONE_NUMBER:
            error_msg = f"Cannot send SMS: 'To' and 'From' numbers cannot be the same ({phone_number})"
            logger.error(error_msg)
            return {
                'success': False,
                'message_sid': None,
                'error': error_msg,
                'provider': 'twilio'
            }
        
        sms = twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        
        logger.info(f"Twilio SMS sent successfully to {phone_number}. SID: {sms.sid}")
        return {
            'success': True,
            'message_sid': sms.sid,
            'error': None,
            'provider': 'twilio'
        }
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Twilio SMS error: {error_msg}")
        
        # Provide helpful error messages
        if "timeout" in error_msg.lower() or "Connection" in error_msg:
            error_msg = f"Twilio connection timeout: Cannot reach Twilio API. Check network/firewall."
        
        return {
            'success': False,
            'message_sid': None,
            'error': f"Twilio: {error_msg}",
            'provider': 'twilio'
        }


def send_blood_request_sms(phone_number, blood_type, location, urgency):
    """
    Send SMS notification about blood request to a donor
    Uses the configured SMS provider (Sparrow SMS or Twilio)
    
    Args:
        phone_number: Recipient's phone number (with country code e.g., +977XXXXXXXXXX)
        blood_type: Blood type needed (e.g., 'AB+')
        location: Location/district of the request
        urgency: Urgency level (Critical, High, Medium, Low)
    
    Returns:
        bool: True if SMS sent successfully, False otherwise
    """
    message = f"🩸 URGENT BLOOD REQUEST 🩸\n\nBlood Type: {blood_type}\nLocation: {location}\nUrgency: {urgency}\n\nYour blood type matches! Please help save lives. Contact the hospital immediately.\n\nReply STOP to unsubscribe."
    
    result = send_sms(phone_number, message)
    return result['success']


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


def send_sms(phone_number, message):
    """
    Send a generic SMS message to a phone number
    Automatically tries Sparrow SMS (Nepal) first, then falls back to Twilio
    
    Args:
        phone_number: Recipient's phone number (with country code e.g., +977XXXXXXXXXX)
        message: Message text to send
    
    Returns:
        dict: {
            'success': bool,
            'message_sid': str or None,
            'error': str or None,
            'provider': str or None
        }
    """
    if not SMS_ENABLED:
        logger.info(f"SMS disabled - would send to {phone_number}: {message[:50]}...")
        return {
            'success': False,
            'message_sid': None,
            'error': 'SMS service not enabled. Configure Sparrow SMS or Twilio.',
            'provider': None
        }
    
    if not phone_number:
        return {
            'success': False,
            'message_sid': None,
            'error': 'Phone number is required',
            'provider': None
        }
    
    if not message:
        return {
            'success': False,
            'message_sid': None,
            'error': 'Message text is required',
            'provider': None
        }
    
    # Try Nepal providers first (better connectivity)
    if SPARROW_ENABLED:
        result = _send_sms_sparrow(phone_number, message)
        if result['success']:
            return result
        logger.warning(f"Sparrow SMS failed, trying next provider: {result['error']}")
    
    if SMS_PASAL_ENABLED:
        result = _send_sms_sms_pasal(phone_number, message)
        if result['success']:
            return result
        logger.warning(f"SMS Pasal failed, trying next provider: {result['error']}")
    
    # Try Twilio as fallback
    if TWILIO_ENABLED:
        result = _send_sms_twilio(phone_number, message)
        return result
    
    # Both providers failed or not configured
    return {
        'success': False,
        'message_sid': None,
        'error': 'All SMS providers failed or not configured',
        'provider': None
    }


def send_bulk_sms(phone_numbers, message):
    """
    Send SMS to multiple phone numbers
    
    Args:
        phone_numbers: List of phone numbers (with country code)
        message: Message text to send
    
    Returns:
        dict: {
            'success_count': int,
            'failed_count': int,
            'results': list of individual results
        }
    """
    results = {
        'success_count': 0,
        'failed_count': 0,
        'results': []
    }
    
    for phone_number in phone_numbers:
        result = send_sms(phone_number, message)
        results['results'].append({
            'phone_number': phone_number,
            'success': result['success'],
            'message_sid': result['message_sid'],
            'error': result['error']
        })
        
        if result['success']:
            results['success_count'] += 1
        else:
            results['failed_count'] += 1
    
    logger.info(f"Bulk SMS results - Success: {results['success_count']}, Failed: {results['failed_count']}")
    return results
