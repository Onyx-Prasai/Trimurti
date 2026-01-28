import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodhub.settings')
django.setup()

from api.models import DonorProfile

print("Current Referral Codes:")
print("=" * 50)
for donor in DonorProfile.objects.all():
    print(f"{donor.user.username:15} → {donor.referral_code}")
    
print("\n" + "=" * 50)
print("✓ All referral codes are now simple and easy to type!")
print("\nHow to use:")
print("1. Copy your referral code from your profile")
print("2. Share it with friends")  
print("3. Friends enter it during registration")
print("4. You get 100 points when they donate!")
