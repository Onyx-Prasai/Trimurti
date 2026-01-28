"""
Update existing donor referral codes to simple format
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodhub.settings')
django.setup()

from api.models import DonorProfile, generate_referral_code

def update_referral_codes():
    """Update all existing donors with new simple referral codes"""
    
    donors = DonorProfile.objects.all()
    updated = 0
    
    print(f"Updating {donors.count()} donor referral codes...")
    print("-" * 50)
    
    for donor in donors:
        old_code = donor.referral_code
        
        # Generate new unique code
        while True:
            new_code = generate_referral_code()
            if not DonorProfile.objects.filter(referral_code=new_code).exists():
                break
        
        donor.referral_code = new_code
        donor.save()
        
        print(f"Updated: {donor.user.username}")
        print(f"  Old: {old_code}")
        print(f"  New: {new_code}")
        print()
        
        updated += 1
    
    print("-" * 50)
    print(f"✓ Updated {updated} referral codes successfully!")
    print()
    print("Sample new referral codes:")
    for donor in DonorProfile.objects.all()[:3]:
        print(f"  - {donor.user.username}: {donor.referral_code}")

if __name__ == '__main__':
    update_referral_codes()
