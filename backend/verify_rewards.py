import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodhub.settings')
django.setup()

from api.models import DiscountReward, MedicineReward

print(f'Discount Rewards: {DiscountReward.objects.count()}')
print(f'Medicine Rewards: {MedicineReward.objects.count()}')
print('\nSample Discounts:')
for d in DiscountReward.objects.all()[:3]:
    print(f'  - {d.name} at {d.business_name}')
print('\nSample Medicines:')
for m in MedicineReward.objects.all()[:3]:
    print(f'  - {m.name} ({m.points_cost} points)')
