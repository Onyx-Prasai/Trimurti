"""
Django management command to test Twilio API connection
Usage: python manage.py test_twilio_connection
"""
from django.core.management.base import BaseCommand
import socket
import requests
from django.conf import settings


class Command(BaseCommand):
    help = 'Test connection to Twilio API'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('\n🔍 Testing Twilio API Connection...\n'))
        
        # Test 1: Check if Twilio is configured
        twilio_account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        twilio_auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        twilio_phone = getattr(settings, 'TWILIO_PHONE_NUMBER', None)
        
        self.stdout.write('1. Checking Twilio Configuration:')
        if twilio_account_sid:
            self.stdout.write(self.style.SUCCESS(f'   ✅ Account SID: {twilio_account_sid[:10]}...'))
        else:
            self.stdout.write(self.style.ERROR('   ❌ Account SID: Not configured'))
        
        if twilio_auth_token:
            self.stdout.write(self.style.SUCCESS(f'   ✅ Auth Token: {"*" * len(twilio_auth_token)}'))
        else:
            self.stdout.write(self.style.ERROR('   ❌ Auth Token: Not configured'))
        
        if twilio_phone:
            self.stdout.write(self.style.SUCCESS(f'   ✅ Phone Number: {twilio_phone}'))
        else:
            self.stdout.write(self.style.ERROR('   ❌ Phone Number: Not configured'))
        
        self.stdout.write('')
        
        # Test 2: Check internet connectivity
        self.stdout.write('2. Testing Internet Connectivity:')
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            self.stdout.write(self.style.SUCCESS('   ✅ Internet connection: OK'))
        except OSError:
            self.stdout.write(self.style.ERROR('   ❌ Internet connection: FAILED'))
            self.stdout.write(self.style.WARNING('   ⚠️  No internet connection detected'))
        
        self.stdout.write('')
        
        # Test 3: Test DNS resolution
        self.stdout.write('3. Testing DNS Resolution:')
        try:
            socket.gethostbyname('api.twilio.com')
            self.stdout.write(self.style.SUCCESS('   ✅ DNS resolution for api.twilio.com: OK'))
        except socket.gaierror:
            self.stdout.write(self.style.ERROR('   ❌ DNS resolution: FAILED'))
            self.stdout.write(self.style.WARNING('   ⚠️  Cannot resolve api.twilio.com'))
        
        self.stdout.write('')
        
        # Test 4: Test HTTPS connection to Twilio
        self.stdout.write('4. Testing HTTPS Connection to Twilio:')
        try:
            response = requests.get(
                'https://api.twilio.com',
                timeout=10,
                headers={'User-Agent': 'BloodHub-Test/1.0'}
            )
            self.stdout.write(self.style.SUCCESS(f'   ✅ HTTPS connection: OK (Status: {response.status_code})'))
        except requests.exceptions.Timeout:
            self.stdout.write(self.style.ERROR('   ❌ HTTPS connection: TIMEOUT'))
            self.stdout.write(self.style.WARNING('   ⚠️  Connection to Twilio API timed out'))
            self.stdout.write(self.style.WARNING('   Possible causes:'))
            self.stdout.write('      - Firewall blocking HTTPS connections')
            self.stdout.write('      - VPN or proxy issues')
            self.stdout.write('      - Network restrictions')
            self.stdout.write('      - Slow internet connection')
        except requests.exceptions.ConnectionError as e:
            self.stdout.write(self.style.ERROR(f'   ❌ HTTPS connection: FAILED'))
            self.stdout.write(self.style.ERROR(f'   Error: {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ HTTPS connection: ERROR'))
            self.stdout.write(self.style.ERROR(f'   Error: {str(e)}'))
        
        self.stdout.write('')
        
        # Test 5: Test Twilio API authentication
        if twilio_account_sid and twilio_auth_token:
            self.stdout.write('5. Testing Twilio API Authentication:')
            try:
                from twilio.rest import Client
                client = Client(twilio_account_sid, twilio_auth_token)
                account = client.api.accounts(twilio_account_sid).fetch()
                self.stdout.write(self.style.SUCCESS(f'   ✅ Authentication: OK'))
                self.stdout.write(f'   Account Status: {account.status}')
                self.stdout.write(f'   Account Type: {account.type}')
            except Exception as e:
                error_msg = str(e)
                if "timeout" in error_msg.lower() or "Connection" in error_msg:
                    self.stdout.write(self.style.ERROR('   ❌ Authentication: CONNECTION TIMEOUT'))
                    self.stdout.write(self.style.WARNING('   ⚠️  Cannot connect to Twilio API'))
                else:
                    self.stdout.write(self.style.ERROR(f'   ❌ Authentication: FAILED'))
                    self.stdout.write(self.style.ERROR(f'   Error: {error_msg}'))
        else:
            self.stdout.write('5. Testing Twilio API Authentication:')
            self.stdout.write(self.style.WARNING('   ⚠️  Skipped (credentials not configured)'))
        
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('📋 Troubleshooting Tips:'))
        self.stdout.write('   1. Check your internet connection')
        self.stdout.write('   2. Disable VPN if enabled')
        self.stdout.write('   3. Check firewall settings (allow HTTPS to api.twilio.com)')
        self.stdout.write('   4. Try using a different network')
        self.stdout.write('   5. Check if your ISP blocks Twilio')
        self.stdout.write('   6. For Nepal: Some ISPs may block international API calls')
        self.stdout.write('')
