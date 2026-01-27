import secrets
from django.core.management.base import BaseCommand
from api.models import Hospital
from api.authentication import hash_api_key


class Command(BaseCommand):
    help = "Create a demo hospital and API key for the BloodSync prototype."

    def add_arguments(self, parser):
        parser.add_argument('--code', default='HSP-001', help='Hospital code identifier')
        parser.add_argument('--name', default='Demo General Hospital', help='Hospital name')
        parser.add_argument('--city', default='Kathmandu', help='City')

    def handle(self, *args, **options):
        raw_key = secrets.token_urlsafe(24)
        api_key_hash = hash_api_key(raw_key)

        hospital, created = Hospital.objects.update_or_create(
            code=options['code'],
            defaults={
                'name': options['name'],
                'city': options['city'],
                'api_key_hash': api_key_hash,
                'is_active': True,
            },
        )

        self.stdout.write(self.style.SUCCESS('Hospital ready:'))
        self.stdout.write(f"  id: {hospital.id}")
        self.stdout.write(f"  code: {hospital.code}")
        self.stdout.write(f"  name: {hospital.name}")
        self.stdout.write(f"  city: {hospital.city}")
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS('Use this API key in X-API-Key header:'))
        self.stdout.write(f"  {raw_key}")
