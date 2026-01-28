"""
Standalone script to test SMS sending
Run: python test_sms_standalone.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodhub.settings')
django.setup()

from api.sms_service import send_blood_request_sms

if __name__ == '__main__':
    # Replace with your verified phone number
    phone_number = input("Enter phone number (with country code, e.g., +1234567890): ").strip()
    
    print(f"\n📱 Sending test SMS to {phone_number}...")
    
    result = send_blood_request_sms(
        phone_number=phone_number,
        blood_type="O+",
        location="Kathmandu",
        urgency="High"
    )
    
    if result:
        print("✅ SMS sent successfully! Check your phone.")
    else:
        print("❌ Failed to send SMS. Check the error logs above.")
