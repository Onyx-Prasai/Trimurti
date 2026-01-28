"""
Django management command to send SMS messages via Twilio
Usage: 
  python manage.py test_sms <phone_number> [--message "Your message"]
  python manage.py test_sms <phone_number> --blood-request
"""
from django.core.management.base import BaseCommand
from api.sms_service import send_sms, send_blood_request_sms, TWILIO_ENABLED


class Command(BaseCommand):
    help = 'Send SMS messages using Twilio'

    def add_arguments(self, parser):
        parser.add_argument(
            'phone_number',
            type=str,
            help='Phone number to send SMS to (with country code, e.g., +1234567890)'
        )
        parser.add_argument(
            '--message',
            type=str,
            help='Custom message to send'
        )
        parser.add_argument(
            '--blood-request',
            action='store_true',
            help='Send a blood request SMS template'
        )
        parser.add_argument(
            '--blood-type',
            type=str,
            default='O+',
            help='Blood type for blood request message (default: O+)'
        )
        parser.add_argument(
            '--location',
            type=str,
            default='Kathmandu',
            help='Location for blood request message (default: Kathmandu)'
        )
        parser.add_argument(
            '--urgency',
            type=str,
            default='High',
            choices=['Critical', 'High', 'Medium', 'Low'],
            help='Urgency level for blood request (default: High)'
        )

    def handle(self, *args, **options):
        phone_number = options['phone_number']
        custom_message = options.get('message')
        blood_request = options.get('blood_request', False)

        self.stdout.write(self.style.WARNING(f'\n📱 SMS Service Status: {"✅ Enabled" if TWILIO_ENABLED else "❌ Disabled"}'))
        
        if not TWILIO_ENABLED:
            self.stdout.write(self.style.ERROR('\n❌ SMS service is disabled!'))
            self.stdout.write(self.style.WARNING('Make sure Twilio credentials are set in .env file'))
            return

        self.stdout.write(f'Phone Number: {phone_number}\n')

        # Determine which type of SMS to send
        if blood_request:
            blood_type = options['blood_type']
            location = options['location']
            urgency = options['urgency']
            
            self.stdout.write(self.style.WARNING('Sending Blood Request SMS...'))
            self.stdout.write(f'Blood Type: {blood_type}')
            self.stdout.write(f'Location: {location}')
            self.stdout.write(f'Urgency: {urgency}\n')
            
            result = send_blood_request_sms(phone_number, blood_type, location, urgency)
            success = result
        else:
            # Send custom message or default test message
            if custom_message:
                message = custom_message
            else:
                message = "🧪 Test SMS from Blood Hub Nepal\n\nThis is a test message to verify SMS functionality."
            
            self.stdout.write(self.style.WARNING('Sending Custom SMS...'))
            self.stdout.write(f'Message: {message[:50]}...\n')
            
            result = send_sms(phone_number, message)
            success = result['success']
            
            if success:
                self.stdout.write(self.style.SUCCESS(f'✅ SMS sent successfully!'))
                self.stdout.write(self.style.SUCCESS(f'Message SID: {result["message_sid"]}'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ Failed to send SMS'))
                self.stdout.write(self.style.ERROR(f'Error: {result["error"]}'))
                return

        if success:
            self.stdout.write(self.style.SUCCESS('\n✅ SMS sent successfully!'))
            self.stdout.write(self.style.SUCCESS('Check your phone for the message.'))
        else:
            self.stdout.write(self.style.ERROR('\n❌ Failed to send SMS'))
            self.stdout.write(self.style.WARNING('\nTroubleshooting:'))
            self.stdout.write('  1. Verify Twilio credentials in .env file')
            self.stdout.write('  2. Phone number must be verified (for trial accounts)')
            self.stdout.write('  3. Phone number must be in E.164 format (+1234567890)')
            self.stdout.write('  4. Check Twilio console for account status')
