from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class DonorProfile(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor_profile')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    points = models.IntegerField(default=0)
    last_donation_date = models.DateField(null=True, blank=True)
    referral_code = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    total_donations = models.IntegerField(default=0)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, default='Kathmandu')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def can_donate(self):
        """Check if donor can donate (56 days have passed since last donation)"""
        if not self.last_donation_date:
            return True
        days_since = (timezone.now().date() - self.last_donation_date).days
        return days_since >= 56
    
    def days_until_next_donation(self):
        """Calculate days until next donation is allowed"""
        if not self.last_donation_date:
            return 0
        days_since = (timezone.now().date() - self.last_donation_date).days
        return max(0, 56 - days_since)
    
    def lives_saved(self):
        """Calculate lives saved (1 donation = 3 lives)"""
        return self.total_donations * 3
    
    def get_badges(self):
        """Get earned badges"""
        badges = []
        if self.total_donations >= 1:
            badges.append('First Drop')
        if self.total_donations >= 5:
            badges.append('Life Saver')
        return badges
    
    def __str__(self):
        return f"{self.user.username} - {self.blood_group}"


class HospitalReq(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    CITIES = [
        ('Kathmandu', 'Kathmandu'),
        ('Bhaktapur', 'Bhaktapur'),
        ('Lalitpur', 'Lalitpur'),
    ]
    
    hospital_id = models.CharField(max_length=50, unique=True)
    hospital_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100, choices=CITIES)
    blood_type_needed = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    units_needed = models.IntegerField(default=1)
    is_critical = models.BooleanField(default=False)
    contact_phone = models.CharField(max_length=15)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.hospital_name} - {self.blood_type_needed}"


class BloodBank(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    operating_hours = models.CharField(max_length=200, default='9 AM - 5 PM')
    
    def __str__(self):
        return self.name


class Donation(models.Model):
    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE, related_name='donations')
    hospital = models.ForeignKey(HospitalReq, on_delete=models.SET_NULL, null=True, blank=True)
    donation_date = models.DateField()
    points_awarded = models.IntegerField(default=100)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.donor.user.username} - {self.donation_date}"


class StoreItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    points_cost = models.IntegerField()
    image = models.ImageField(upload_to='store_items/', null=True, blank=True)
    stock = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Redemption(models.Model):
    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE, related_name='redemptions')
    item = models.ForeignKey(StoreItem, on_delete=models.CASCADE)
    points_used = models.IntegerField()
    redeemed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ])
    
    def __str__(self):
        return f"{self.donor.user.username} - {self.item.name}"

