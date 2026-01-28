import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodhub.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@bloodhub.local', 'admin123')
    print("✓ Superuser 'admin' created successfully!")
    print("  Username: admin")
    print("  Email: admin@bloodhub.local")
    print("  Password: admin123")
else:
    print("✗ Superuser 'admin' already exists")
