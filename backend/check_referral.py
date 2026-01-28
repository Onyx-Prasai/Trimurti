import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodhub.settings')
django.setup()

from api.models import DonorProfile
from django.contrib.auth import get_user_model

User = get_user_model()

# Get or create a test donor
users = User.objects.filter(user_type='base_user')
if users.exists():
    test_user = users.first()
    donor = DonorProfile.objects.get(user=test_user)
    print(f"Sample Donor: {test_user.username}")
    print(f"Referral Code: {donor.referral_code}")
    print(f"\nTo test the referral system:")
    print(f"1. Register a new user with referral code: {donor.referral_code}")
    print(f"2. When the new user makes their first donation, {test_user.username} will get 100 bonus points")
    print(f"\nCurrent donor points: {donor.points}")
    print(f"Total referrals: {donor.referrals.count()}")
else:
    print("No donors found. Register a user first to test the referral system.")
