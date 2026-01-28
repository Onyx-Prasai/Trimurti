import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodhub.settings')
django.setup()

from django.test import RequestFactory, Client
from api.models import DonorProfile
from django.contrib.auth import get_user_model

User = get_user_model()

# Get a referral code from an existing donor
existing_donors = DonorProfile.objects.all()
if existing_donors.exists():
    referrer = existing_donors.first()
    referral_code = str(referrer.referral_code)
    print(f"Testing with referral code: {referral_code}")
    print(f"Referrer: {referrer.user.username}")
    print()
    
    # Test registration with referral code
    client = Client()
    
    test_data = {
        'username': 'test_referred_user',
        'email': 'testreferred@test.com',
        'password': 'testpass123',
        'password2': 'testpass123',
        'first_name': 'Test',
        'last_name': 'Referred',
        'referral_code': referral_code
    }
    
    print("Test data:", json.dumps(test_data, indent=2))
    print()
    
    # Try to register
    try:
        response = client.post(
            '/api/auth/register/',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("\n✓ Registration successful!")
            # Check if referral was linked
            new_user = User.objects.get(username='test_referred_user')
            new_donor = DonorProfile.objects.get(user=new_user)
            if new_donor.referred_by:
                print(f"✓ Referral linked! Referred by: {new_donor.referred_by.user.username}")
            else:
                print("✗ Referral NOT linked!")
        else:
            print("\n✗ Registration failed!")
            
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    # Cleanup
    try:
        User.objects.filter(username='test_referred_user').delete()
        print("\nCleanup: Test user deleted")
    except:
        pass
else:
    print("No donors found. Create a donor first.")
