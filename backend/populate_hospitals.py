import os
import django
import hashlib
from decimal import Decimal
from datetime import datetime
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodhub.settings')
django.setup()

from api.models import Hospital, BloodStock, HospitalReq

# Clear existing data
Hospital.objects.all().delete()
BloodStock.objects.all().delete()
HospitalReq.objects.all().delete()

# Hospital names for variety
hospital_types = [
    'Medical Center', 'Hospital', 'Clinical Hospital', 'Teaching Hospital',
    'Trauma Center', 'Surgery Institute', 'Health Complex', 'Nursing Home',
    'Care Center', 'Emergency Hospital', 'District Hospital'
]

# Nepal cities
nepal_cities = [
    'Kathmandu', 'Lalitpur', 'Bhaktapur', 'Kavre', 'Nuwakot',
    'Rasuwa', 'Sindhuli', 'Ramechhap', 'Dolakha', 'Makwanpur',
    'Ilam', 'Jhapa', 'Morang', 'Sunsari', 'Dhankuta',
    'Terhathum', 'Panchthar', 'Udayapur', 'Sankhuwasabha', 'Sindhupalchok',
    'Gorkha', 'Lamjung', 'Tanahu', 'Chitwan', 'Nawalpur',
    'Parsa', 'Bara', 'Rautahat', 'Gulmi', 'Arghakhanchi',
    'Palpa', 'Dang', 'Banke', 'Bardiya', 'Surkhet',
    'Salyan', 'Pyuthan', 'Rolpa', 'Rukum', 'Dailekh',
    'Jumla', 'Kalikot', 'Dolpa', 'Jajarkot', 'Achham',
    'Bajura', 'Bajhang', 'Doti', 'Kailali', 'Kanchanpur'
]

hospital_names_prefix = [
    'Kathmandu', 'Patan', 'Bhaktapur', 'Bir', 'Nepal', 'Valley',
    'City', 'Central', 'District', 'Regional', 'Provincial',
    'Modern', 'Advanced', 'State', 'Municipal', 'Community'
]

# Generate 100 hospitals
hospitals_data = []
import random
random.seed(42)

for i in range(1, 101):
    city = nepal_cities[(i - 1) % len(nepal_cities)]
    prefix = hospital_names_prefix[(i - 1) % len(hospital_names_prefix)]
    hospital_type = hospital_types[(i - 1) % len(hospital_types)]
    
    name = f"{prefix} {hospital_type} {i}" if i % 3 == 0 else f"{city.split()[0]} {hospital_type}"
    
    # Generate coordinates around Nepal
    base_lat = 27.7 + random.uniform(-2, 2)
    base_lon = 85.3 + random.uniform(-3, 3)
    
    # Random blood stock (10-50 units per type)
    blood_stock = {
        'A+': random.randint(8, 35),
        'A-': random.randint(2, 10),
        'B+': random.randint(8, 40),
        'B-': random.randint(2, 8),
        'AB+': random.randint(2, 8),
        'AB-': random.randint(1, 4),
        'O+': random.randint(15, 50),
        'O-': random.randint(5, 15),
    }
    
    hospitals_data.append({
        'code': f'HOSP{i:03d}',
        'name': name,
        'city': city,
        'address': f'{city}, Nepal (Hospital ID: {i})',
        'latitude': Decimal(str(round(base_lat, 4))),
        'longitude': Decimal(str(round(base_lon, 4))),
        'blood_stock': blood_stock
    })

# Create hospitals and blood stocks
hospitals = []
for hospital_data in hospitals_data:
    blood_stock_data = hospital_data.pop('blood_stock')
    
    # Create API key hash (simple hash for demo)
    api_key = f"api_key_{hospital_data['code']}"
    api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    hospital = Hospital.objects.create(
        **hospital_data,
        api_key_hash=api_key_hash,
        is_active=True
    )
    hospitals.append(hospital)
    
    # Create blood stocks for this hospital
    for blood_group, units in blood_stock_data.items():
        BloodStock.objects.create(
            hospital=hospital,
            blood_group=blood_group,
            blood_product_type='whole_blood',
            units_available=units
        )
    
    print(f"[+] Created {hospital.name} with {sum(blood_stock_data.values())} total blood units")

# Create hospital requirements (hospitals needing blood) - 30 requests
blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
blood_products = ['whole_blood', 'plasma', 'platelets']
hospital_reqs_data = []

for i in range(1, 31):
    city = nepal_cities[(i - 1) % len(nepal_cities)]
    base_lat = 27.7 + random.uniform(-2, 2)
    base_lon = 85.3 + random.uniform(-3, 3)
    
    hospital_reqs_data.append({
        'hospital_id': f'REQ{i:03d}',
        'hospital_name': f'{city} Emergency Request {i}',
        'district': city,
        'blood_type_needed': random.choice(blood_types),
        'blood_product_needed': random.choice(blood_products),
        'units_needed': random.randint(2, 8),
        'is_critical': random.choice([True, True, False]),  # 67% critical
        'contact_phone': f'+977-{random.randint(1, 14)}-{random.randint(1000000, 9999999)}',
        'address': f'{city}, Nepal (Request ID: {i})',
        'latitude': Decimal(str(round(base_lat, 4))),
        'longitude': Decimal(str(round(base_lon, 4))),
    })

# Create hospital requirements
for req_data in hospital_reqs_data:
    req = HospitalReq.objects.create(**req_data)
    print(f"[+] Created requirement: {req.hospital_name} needs {req.units_needed} units of {req.blood_type_needed} (Critical: {req.is_critical})")

print("\n" + "="*60)
print("SYNTHETIC DATA CREATED SUCCESSFULLY!")
print("="*60)
print(f"\nHospitals Created: {len(hospitals)}")
print(f"Hospital Requirements Created: {len(hospital_reqs_data)}")
print(f"\nTotal Blood Stock Across Hospitals:")
from django.db.models import Sum
total_units = BloodStock.objects.aggregate(
    total=Sum('units_available')
)['total'] or 0
print(f"  {total_units} total units")
print(f"\nCritical Requests:")
critical_reqs = HospitalReq.objects.filter(is_critical=True).count()
print(f"  {critical_reqs} hospitals with critical blood needs")

# Summary statistics
avg_stock = BloodStock.objects.values('hospital').annotate(
    total=Sum('units_available')
).aggregate(avg=django.db.models.Avg('total'))['avg'] or 0
print(f"\nAverage Stock Per Hospital: {avg_stock:.1f} units")
