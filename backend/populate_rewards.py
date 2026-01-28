"""
Populate sample rewards (discounts and medicines) for the Blood Hub Nepal system.
"""

import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodhub.settings')
django.setup()

from api.models import DiscountReward, MedicineReward


def populate_discount_rewards():
    """Add restaurants, cafes, and other discount rewards"""
    
    discounts = [
        # Restaurants
        {
            'name': '15% Off at Bhojan Griha',
            'business_name': 'Bhojan Griha Restaurant',
            'business_type': 'Restaurant',
            'description': 'Get 15% off on your total bill at Bhojan Griha, one of Kathmandu\'s finest traditional Nepali restaurants. Valid for dine-in only.',
            'discount_percentage': 15,
            'points_cost': 150,
            'coupon_code': 'BLOOD15-BHOJAN',
            'valid_until': date.today() + timedelta(days=180),
            'stock': 50,
        },
        {
            'name': '20% Off at Fire and Ice Pizzeria',
            'business_name': 'Fire and Ice Pizzeria',
            'business_type': 'Restaurant',
            'description': 'Enjoy 20% discount on all pizzas and Italian dishes at Fire and Ice Pizzeria. Valid at all Kathmandu locations.',
            'discount_percentage': 20,
            'points_cost': 200,
            'coupon_code': 'BLOOD20-FIREICE',
            'valid_until': date.today() + timedelta(days=180),
            'stock': 40,
        },
        {
            'name': '10% Off at Roadhouse Cafe',
            'business_name': 'Roadhouse Cafe',
            'business_type': 'Restaurant',
            'description': '10% off on your total bill at Roadhouse Cafe. Enjoy American-style burgers, steaks, and more!',
            'discount_percentage': 10,
            'points_cost': 100,
            'coupon_code': 'BLOOD10-ROADHOUSE',
            'valid_until': date.today() + timedelta(days=180),
            'stock': 60,
        },
        {
            'name': '25% Off at Kaiser Cafe',
            'business_name': 'Kaiser Cafe',
            'business_type': 'Cafe',
            'description': 'Get 25% off at Kaiser Cafe in Kathmandu. Perfect for coffee, pastries, and light meals in a serene garden setting.',
            'discount_percentage': 25,
            'points_cost': 250,
            'coupon_code': 'BLOOD25-KAISER',
            'valid_until': date.today() + timedelta(days=180),
            'stock': 30,
        },
        
        # Cafes
        {
            'name': '15% Off at Himalayan Java Coffee',
            'business_name': 'Himalayan Java Coffee',
            'business_type': 'Cafe',
            'description': '15% discount on all beverages and snacks at Himalayan Java Coffee. Valid at all outlets across Nepal.',
            'discount_percentage': 15,
            'points_cost': 150,
            'coupon_code': 'BLOOD15-HIMJAVA',
            'valid_until': date.today() + timedelta(days=180),
            'stock': 100,
        },
        {
            'name': '20% Off at The Bakery Cafe',
            'business_name': 'The Bakery Cafe',
            'business_type': 'Cafe',
            'description': 'Enjoy 20% off on all bakery items and beverages at The Bakery Cafe. Fresh pastries, cakes, and artisan coffee.',
            'discount_percentage': 20,
            'points_cost': 200,
            'coupon_code': 'BLOOD20-BAKERY',
            'valid_until': date.today() + timedelta(days=180),
            'stock': 50,
        },
        {
            'name': '10% Off at Yellow House Coffee',
            'business_name': 'Yellow House Coffee',
            'business_type': 'Cafe',
            'description': '10% discount at Yellow House Coffee in Jhamsikhel. Great coffee and cozy ambiance.',
            'discount_percentage': 10,
            'points_cost': 100,
            'coupon_code': 'BLOOD10-YELLOW',
            'valid_until': date.today() + timedelta(days=180),
            'stock': 40,
        },
        
        # Fast Food
        {
            'name': '15% Off at KFC Nepal',
            'business_name': 'KFC Nepal',
            'business_type': 'Fast Food',
            'description': 'Get 15% off on your order at KFC Nepal. Valid at all outlets.',
            'discount_percentage': 15,
            'points_cost': 150,
            'coupon_code': 'BLOOD15-KFC',
            'valid_until': date.today() + timedelta(days=180),
            'stock': 80,
        },
        {
            'name': '10% Off at Pizza Hut Nepal',
            'business_name': 'Pizza Hut Nepal',
            'business_type': 'Fast Food',
            'description': '10% discount on all pizzas and sides at Pizza Hut Nepal.',
            'discount_percentage': 10,
            'points_cost': 100,
            'coupon_code': 'BLOOD10-PIZZAHUT',
            'valid_until': date.today() + timedelta(days=180),
            'stock': 70,
        },
        
        # Other Businesses
        {
            'name': '20% Off at Labim Mall Food Court',
            'business_name': 'Labim Mall Food Court',
            'business_type': 'Food Court',
            'description': '20% off at any restaurant in Labim Mall Food Court. Wide variety of cuisines available.',
            'discount_percentage': 20,
            'points_cost': 200,
            'coupon_code': 'BLOOD20-LABIM',
            'valid_until': date.today() + timedelta(days=180),
            'stock': 60,
        },
    ]
    
    created_count = 0
    for discount_data in discounts:
        discount, created = DiscountReward.objects.get_or_create(
            coupon_code=discount_data['coupon_code'],
            defaults=discount_data
        )
        if created:
            created_count += 1
            print(f"Created: {discount.name}")
        else:
            print(f"Already exists: {discount.name}")
    
    print(f"\nTotal discount rewards created: {created_count}/{len(discounts)}")


def populate_medicine_rewards():
    """Add pharmacy medicines and healthcare products"""
    
    medicines = [
        # Pain Relief & Common Medicines
        {
            'name': 'Paracetamol 500mg (Strip of 10)',
            'description': 'Paracetamol tablets for pain relief and fever reduction. 500mg strength, pack of 10 tablets.',
            'category': 'Pain Relief',
            'points_cost': 50,
            'provider': 'Nepal Pharmacy',
            'stock': 200,
        },
        {
            'name': 'Ibuprofen 400mg (Strip of 10)',
            'description': 'Anti-inflammatory and pain relief medication. 400mg strength, pack of 10 tablets.',
            'category': 'Pain Relief',
            'points_cost': 80,
            'provider': 'Nepal Pharmacy',
            'stock': 150,
        },
        {
            'name': 'Cetrizine 10mg (Strip of 10)',
            'description': 'Antihistamine for allergy relief. 10mg strength, pack of 10 tablets.',
            'category': 'Allergy Medicine',
            'points_cost': 60,
            'provider': 'Nepal Pharmacy',
            'stock': 180,
        },
        {
            'name': 'Vitamin C 500mg (Bottle of 30)',
            'description': 'Vitamin C supplement tablets for immune support. 500mg strength, bottle of 30 tablets.',
            'category': 'Vitamin Supplement',
            'points_cost': 150,
            'provider': 'HealthCare Plus',
            'stock': 100,
        },
        {
            'name': 'Multivitamin Tablets (Bottle of 30)',
            'description': 'Complete multivitamin supplement with essential vitamins and minerals. Bottle of 30 tablets.',
            'category': 'Vitamin Supplement',
            'points_cost': 200,
            'provider': 'HealthCare Plus',
            'stock': 120,
        },
        
        # Iron & Blood Health
        {
            'name': 'Iron + Folic Acid Tablets (Bottle of 30)',
            'description': 'Iron supplement with folic acid for blood health. Essential for blood donors. Bottle of 30 tablets.',
            'category': 'Blood Health Supplement',
            'points_cost': 180,
            'provider': 'HealthCare Plus',
            'stock': 150,
        },
        {
            'name': 'Vitamin B Complex (Bottle of 30)',
            'description': 'B-Complex vitamins for energy and blood cell formation. Bottle of 30 tablets.',
            'category': 'Vitamin Supplement',
            'points_cost': 170,
            'provider': 'HealthCare Plus',
            'stock': 130,
        },
        
        # First Aid & Healthcare Items
        {
            'name': 'Digital Thermometer',
            'description': 'Digital thermometer for accurate temperature measurement. LCD display, automatic shut-off.',
            'category': 'Healthcare Device',
            'points_cost': 300,
            'provider': 'MediCare Store',
            'stock': 50,
        },
        {
            'name': 'Blood Pressure Monitor',
            'description': 'Digital blood pressure monitor for home use. Automatic measurement with memory function.',
            'category': 'Healthcare Device',
            'points_cost': 800,
            'provider': 'MediCare Store',
            'stock': 30,
        },
        {
            'name': 'First Aid Kit (Complete)',
            'description': 'Complete first aid kit with bandages, antiseptic, gauze, scissors, and other essentials.',
            'category': 'First Aid',
            'points_cost': 400,
            'provider': 'MediCare Store',
            'stock': 60,
        },
        
        # Digestive Health
        {
            'name': 'Antacid Tablets (Strip of 10)',
            'description': 'Antacid tablets for quick relief from acidity and heartburn. Pack of 10 tablets.',
            'category': 'Digestive Health',
            'points_cost': 70,
            'provider': 'Nepal Pharmacy',
            'stock': 140,
        },
        {
            'name': 'ORS Powder (Pack of 10 Sachets)',
            'description': 'Oral Rehydration Solution powder for dehydration treatment. Pack of 10 sachets.',
            'category': 'Digestive Health',
            'points_cost': 90,
            'provider': 'Nepal Pharmacy',
            'stock': 160,
        },
        
        # Sanitizers & Hygiene
        {
            'name': 'Hand Sanitizer 500ml',
            'description': 'Alcohol-based hand sanitizer. 500ml bottle, kills 99.9% germs.',
            'category': 'Hygiene Product',
            'points_cost': 120,
            'provider': 'Nepal Pharmacy',
            'stock': 200,
        },
        {
            'name': 'Surgical Face Masks (Box of 50)',
            'description': '3-ply disposable surgical face masks. Box of 50 pieces.',
            'category': 'Hygiene Product',
            'points_cost': 250,
            'provider': 'MediCare Store',
            'stock': 80,
        },
        
        # Eye Care
        {
            'name': 'Eye Drops (10ml)',
            'description': 'Lubricating eye drops for dry eye relief. 10ml bottle.',
            'category': 'Eye Care',
            'points_cost': 130,
            'provider': 'Nepal Pharmacy',
            'stock': 90,
        },
    ]
    
    created_count = 0
    for medicine_data in medicines:
        medicine, created = MedicineReward.objects.get_or_create(
            name=medicine_data['name'],
            provider=medicine_data['provider'],
            defaults=medicine_data
        )
        if created:
            created_count += 1
            print(f"Created: {medicine.name}")
        else:
            print(f"Already exists: {medicine.name}")
    
    print(f"\nTotal medicine rewards created: {created_count}/{len(medicines)}")


def main():
    print("=" * 70)
    print("POPULATING DISCOUNT REWARDS (Restaurants & Cafes)")
    print("=" * 70)
    populate_discount_rewards()
    
    print("\n" + "=" * 70)
    print("POPULATING MEDICINE REWARDS (Pharmacy Products)")
    print("=" * 70)
    populate_medicine_rewards()
    
    print("\n" + "=" * 70)
    print("POPULATION COMPLETE!")
    print("=" * 70)


if __name__ == '__main__':
    main()
