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
                'district': 'Kathmandu',
                'address': 'Red Cross Marg, Kathmandu 44600',
                'phone': '+977-1-4415783',
                'latitude': 27.7172,
                'longitude': 85.3240,
            },
            {
                'name': 'Bhaktapur Blood Bank',
                'district': 'Bhaktapur',
                'address': 'Bhaktapur Durbar Square, Bhaktapur',
                'phone': '+977-1-6611234',
                'latitude': 27.6710,
                'longitude': 85.4298,
            },
            {
                'name': 'Lalitpur Blood Center',
                'district': 'Lalitpur',
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
            # Kathmandu Hospitals
            {'hospital_id': 'HOSP001', 'hospital_name': 'Tribhuvan University Teaching Hospital', 'district': 'Kathmandu', 'blood_type_needed': 'O+', 'blood_product_needed': 'whole_blood', 'units_needed': 5, 'is_critical': True, 'contact_phone': '+977-1-4412505', 'address': 'Maharajgunj, Kathmandu', 'latitude': 27.7307, 'longitude': 85.3320},
            {'hospital_id': 'HOSP002', 'hospital_name': 'Bir Hospital', 'district': 'Kathmandu', 'blood_type_needed': 'A+', 'blood_product_needed': 'plasma', 'units_needed': 3, 'is_critical': False, 'contact_phone': '+977-1-4221119', 'address': 'Kantipath, Kathmandu', 'latitude': 27.7106, 'longitude': 85.3158},
            {'hospital_id': 'HOSP003', 'hospital_name': 'Nepal Medical College Teaching Hospital', 'district': 'Kathmandu', 'blood_type_needed': 'B+', 'blood_product_needed': 'platelets', 'units_needed': 4, 'is_critical': False, 'contact_phone': '+977-1-4912405', 'address': 'Attarkhel, Kathmandu', 'latitude': 27.7614, 'longitude': 85.3289},
            {'hospital_id': 'HOSP004', 'hospital_name': 'Kathmandu Medical College', 'district': 'Kathmandu', 'blood_type_needed': 'AB+', 'blood_product_needed': 'whole_blood', 'units_needed': 2, 'is_critical': False, 'contact_phone': '+977-1-6633663', 'address': 'Duwakot, Kathmandu', 'latitude': 27.6939, 'longitude': 85.4067},
            {'hospital_id': 'HOSP005', 'hospital_name': 'National Hospital', 'district': 'Kathmandu', 'blood_type_needed': 'O-', 'blood_product_needed': 'plasma', 'units_needed': 3, 'is_critical': True, 'contact_phone': '+977-1-4010103', 'address': 'Kathmandu, Nepal', 'latitude': 27.7315, 'longitude': 85.3254},
            
            # Bhaktapur Hospitals
            {'hospital_id': 'HOSP006', 'hospital_name': 'Bhaktapur Hospital', 'district': 'Bhaktapur', 'blood_type_needed': 'A+', 'blood_product_needed': 'platelets', 'units_needed': 2, 'is_critical': False, 'contact_phone': '+977-1-6611234', 'address': 'Bhaktapur Durbar Square', 'latitude': 27.6710, 'longitude': 85.4298},
            {'hospital_id': 'HOSP007', 'hospital_name': 'Bhaktapur Eye Hospital', 'district': 'Bhaktapur', 'blood_type_needed': 'B+', 'blood_product_needed': 'whole_blood', 'units_needed': 1, 'is_critical': False, 'contact_phone': '+977-1-6612345', 'address': 'Thani, Bhaktapur', 'latitude': 27.6526, 'longitude': 85.4231},
            
            # Lalitpur Hospitals
            {'hospital_id': 'HOSP008', 'hospital_name': 'Patan Academy of Health Sciences Teaching Hospital', 'district': 'Lalitpur', 'blood_type_needed': 'O+', 'blood_product_needed': 'plasma', 'units_needed': 4, 'is_critical': False, 'contact_phone': '+977-1-5521234', 'address': 'Lalitpur, Nepal', 'latitude': 27.6789, 'longitude': 85.3210},
            {'hospital_id': 'HOSP009', 'hospital_name': 'Amandeep Hospital', 'district': 'Lalitpur', 'blood_type_needed': 'A+', 'blood_product_needed': 'platelets', 'units_needed': 2, 'is_critical': False, 'contact_phone': '+977-1-5544444', 'address': 'Lalitpur', 'latitude': 27.6766, 'longitude': 85.3249},
            
            # Pokhara (Kaski) - Major city in Western Region
            {'hospital_id': 'HOSP010', 'hospital_name': 'Kaski Hopital', 'district': 'Kaski', 'blood_type_needed': 'B+', 'blood_product_needed': 'whole_blood', 'units_needed': 3, 'is_critical': False, 'contact_phone': '+977-61-525555', 'address': 'Pokhara, Kaski', 'latitude': 28.2096, 'longitude': 83.9856},
            {'hospital_id': 'HOSP011', 'hospital_name': 'Western Regional Hospital', 'district': 'Kaski', 'blood_type_needed': 'O+', 'blood_product_needed': 'plasma', 'units_needed': 4, 'is_critical': True, 'contact_phone': '+977-61-410033', 'address': 'Pokhara', 'latitude': 28.2041, 'longitude': 83.9904},
            
            # Morang (Eastern Region)
            {'hospital_id': 'HOSP012', 'hospital_name': 'B.P. Koirala Institute of Health Sciences', 'district': 'Morang', 'blood_type_needed': 'O+', 'blood_product_needed': 'platelets', 'units_needed': 5, 'is_critical': True, 'contact_phone': '+977-23-670080', 'address': 'Dharan, Morang', 'latitude': 26.8133, 'longitude': 87.2641},
            {'hospital_id': 'HOSP013', 'hospital_name': 'Koshi Zonal Hospital', 'district': 'Morang', 'blood_type_needed': 'A+', 'blood_product_needed': 'whole_blood', 'units_needed': 3, 'is_critical': False, 'contact_phone': '+977-23-522633', 'address': 'Biratnagar, Morang', 'latitude': 26.4526, 'longitude': 87.2667},
            
            # Chitwan
            {'hospital_id': 'HOSP014', 'hospital_name': 'Chitwan Medical College Teaching Hospital', 'district': 'Chitwan', 'blood_type_needed': 'B+', 'blood_product_needed': 'plasma', 'units_needed': 3, 'is_critical': False, 'contact_phone': '+977-56-550055', 'address': 'Bharatpur, Chitwan', 'latitude': 27.6833, 'longitude': 84.4458},
            {'hospital_id': 'HOSP015', 'hospital_name': 'Gandaki Medical College Teaching Hospital', 'district': 'Chitwan', 'blood_type_needed': 'O+', 'blood_product_needed': 'whole_blood', 'units_needed': 3, 'is_critical': False, 'contact_phone': '+977-56-540555', 'address': 'Bharatpur, Chitwan', 'latitude': 27.6845, 'longitude': 84.4372},
            
            # Jhapa
            {'hospital_id': 'HOSP016', 'hospital_name': 'Jhapa Hospital', 'district': 'Jhapa', 'blood_type_needed': 'A+', 'blood_product_needed': 'platelets', 'units_needed': 2, 'is_critical': False, 'contact_phone': '+977-23-410410', 'address': 'Damak, Jhapa', 'latitude': 26.6159, 'longitude': 87.7667},
            
            # Sunsari
            {'hospital_id': 'HOSP017', 'hospital_name': 'Sunsari District Hospital', 'district': 'Sunsari', 'blood_type_needed': 'O+', 'blood_product_needed': 'plasma', 'units_needed': 2, 'is_critical': False, 'contact_phone': '+977-25-510010', 'address': 'Inaruwa, Sunsari', 'latitude': 26.6694, 'longitude': 87.1891},
            
            # Ilam
            {'hospital_id': 'HOSP018', 'hospital_name': 'Ilam District Hospital', 'district': 'Ilam', 'blood_type_needed': 'B+', 'blood_product_needed': 'whole_blood', 'units_needed': 1, 'is_critical': False, 'contact_phone': '+977-23-410410', 'address': 'Ilam', 'latitude': 26.9124, 'longitude': 87.9182},
            
            # Dang
            {'hospital_id': 'HOSP019', 'hospital_name': 'Dang Hospital', 'district': 'Dang', 'blood_type_needed': 'A+', 'blood_product_needed': 'plasma', 'units_needed': 2, 'is_critical': False, 'contact_phone': '+977-82-410410', 'address': 'Ghorahi, Dang', 'latitude': 28.2401, 'longitude': 82.5814},
            
            # Banke
            {'hospital_id': 'HOSP020', 'hospital_name': 'Banke District Hospital', 'district': 'Banke', 'blood_type_needed': 'O+', 'blood_product_needed': 'platelets', 'units_needed': 2, 'is_critical': False, 'contact_phone': '+977-81-410410', 'address': 'Nepalgunj, Banke', 'latitude': 28.7041, 'longitude': 81.1133},
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

