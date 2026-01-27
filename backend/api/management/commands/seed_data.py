from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import DonorProfile, HospitalReq, BloodBank, StoreItem


class Command(BaseCommand):
    help = 'Seed initial data for development'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # Create sample blood banks
        blood_banks = [
            {
                'name': 'Nepal Red Cross Society - Kathmandu',
                'city': 'Kathmandu',
                'address': 'Red Cross Marg, Kathmandu 44600',
                'phone': '+977-1-4415783',
                'latitude': 27.7172,
                'longitude': 85.3240,
            },
            {
                'name': 'Bhaktapur Blood Bank',
                'city': 'Bhaktapur',
                'address': 'Bhaktapur Durbar Square, Bhaktapur',
                'phone': '+977-1-6611234',
                'latitude': 27.6710,
                'longitude': 85.4298,
            },
            {
                'name': 'Lalitpur Blood Center',
                'city': 'Lalitpur',
                'address': 'Patan, Lalitpur',
                'phone': '+977-1-5521234',
                'latitude': 27.6766,
                'longitude': 85.3249,
            },
        ]

        for bank_data in blood_banks:
            BloodBank.objects.get_or_create(
                name=bank_data['name'],
                defaults=bank_data
            )

        # Create sample hospital requests
        hospitals = [
            {
                'hospital_id': 'HOSP001',
                'hospital_name': 'Tribhuvan University Teaching Hospital',
                'city': 'Kathmandu',
                'blood_type_needed': 'O+',
                'units_needed': 5,
                'is_critical': True,
                'contact_phone': '+977-1-4412505',
                'address': 'Maharajgunj, Kathmandu',
                'latitude': 27.7307,
                'longitude': 85.3320,
            },
            {
                'hospital_id': 'HOSP002',
                'hospital_name': 'Bir Hospital',
                'city': 'Kathmandu',
                'blood_type_needed': 'A+',
                'units_needed': 3,
                'is_critical': False,
                'contact_phone': '+977-1-4221119',
                'address': 'Kantipath, Kathmandu',
                'latitude': 27.7106,
                'longitude': 85.3158,
            },
        ]

        for hosp_data in hospitals:
            HospitalReq.objects.get_or_create(
                hospital_id=hosp_data['hospital_id'],
                defaults=hosp_data
            )

        # Create store items
        store_items = [
            {
                'name': 'Paracetamol',
                'description': 'Pain relief medicine (500mg)',
                'points_cost': 50,
                'stock': 20,
            },
            {
                'name': 'First Aid Kit',
                'description': 'Complete first aid kit with bandages and antiseptics',
                'points_cost': 200,
                'stock': 10,
            },
            {
                'name': 'Health Checkup Voucher',
                'description': 'Free comprehensive health checkup at partner clinics',
                'points_cost': 300,
                'stock': 5,
            },
            {
                'name': 'Iron Supplements',
                'description': 'Iron tablets to maintain healthy hemoglobin levels',
                'points_cost': 150,
                'stock': 15,
            },
        ]

        for item_data in store_items:
            StoreItem.objects.get_or_create(
                name=item_data['name'],
                defaults=item_data
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded data!'))

