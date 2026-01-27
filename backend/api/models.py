from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

BLOOD_PRODUCT_CHOICES = [
    ('whole_blood', 'Whole Blood'),
    ('plasma', 'Plasma'),
    ('platelets', 'Platelets'),
]


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
    
    DISTRICTS = [
        # Bagmati Province
        ('Kathmandu', 'Kathmandu'),
        ('Bhaktapur', 'Bhaktapur'),
        ('Lalitpur', 'Lalitpur'),
        ('Kavre', 'Kavre'),
        ('Nuwakot', 'Nuwakot'),
        ('Rasuwa', 'Rasuwa'),
        ('Sindhuli', 'Sindhuli'),
        ('Ramechhap', 'Ramechhap'),
        ('Dolakha', 'Dolakha'),
        ('Makwanpur', 'Makwanpur'),
        # Eastern Region
        ('Ilam', 'Ilam'),
        ('Jhapa', 'Jhapa'),
        ('Morang', 'Morang'),
        ('Sunsari', 'Sunsari'),
        ('Dhankuta', 'Dhankuta'),
        ('Terhathum', 'Terhathum'),
        ('Panchthar', 'Panchthar'),
        ('Udayapur', 'Udayapur'),
        ('Sankhuwasabha', 'Sankhuwasabha'),
        ('Sindhupalchok', 'Sindhupalchok'),
        # Central Region
        ('Gorkha', 'Gorkha'),
        ('Lamjung', 'Lamjung'),
        ('Tanahu', 'Tanahu'),
        ('Chitwan', 'Chitwan'),
        ('Nawalpur', 'Nawalpur'),
        ('Parsa', 'Parsa'),
        ('Bara', 'Bara'),
        ('Rautahat', 'Rautahat'),
        ('Gulmi', 'Gulmi'),
        ('Arghakhanchi', 'Arghakhanchi'),
        # Western Region
        ('Palpa', 'Palpa'),
        ('Dang', 'Dang'),
        ('Banke', 'Banke'),
        ('Bardiya', 'Bardiya'),
        ('Surkhet', 'Surkhet'),
        # Mid-Western Region
        ('Salyan', 'Salyan'),
        ('Pyuthan', 'Pyuthan'),
        ('Rolpa', 'Rolpa'),
        ('Rukum', 'Rukum'),
        ('Dailekh', 'Dailekh'),
        ('Jumla', 'Jumla'),
        ('Kalikot', 'Kalikot'),
        ('Dolpa', 'Dolpa'),
        # Far-Western Region
        ('Jajarkot', 'Jajarkot'),
        ('Achham', 'Achham'),
        ('Bajura', 'Bajura'),
        ('Bajhang', 'Bajhang'),
        ('Doti', 'Doti'),
        ('Kailali', 'Kailali'),
        ('Kanchanpur', 'Kanchanpur'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor_profile')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    blood_product_type = models.CharField(max_length=20, choices=BLOOD_PRODUCT_CHOICES, default='whole_blood')
    points = models.IntegerField(default=0)
    last_donation_date = models.DateField(null=True, blank=True)
    referral_code = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    total_donations = models.IntegerField(default=0)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    district = models.CharField(max_length=100, choices=DISTRICTS, default='Kathmandu')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_consent = models.BooleanField(default=False)
    location_verified_at = models.DateTimeField(null=True, blank=True)
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
    
    DISTRICTS = [
        # Bagmati Province
        ('Kathmandu', 'Kathmandu'),
        ('Bhaktapur', 'Bhaktapur'),
        ('Lalitpur', 'Lalitpur'),
        ('Kavre', 'Kavre'),
        ('Nuwakot', 'Nuwakot'),
        ('Rasuwa', 'Rasuwa'),
        ('Sindhuli', 'Sindhuli'),
        ('Ramechhap', 'Ramechhap'),
        ('Dolakha', 'Dolakha'),
        ('Makwanpur', 'Makwanpur'),
        # Eastern Region
        ('Ilam', 'Ilam'),
        ('Jhapa', 'Jhapa'),
        ('Morang', 'Morang'),
        ('Sunsari', 'Sunsari'),
        ('Dhankuta', 'Dhankuta'),
        ('Terhathum', 'Terhathum'),
        ('Panchthar', 'Panchthar'),
        ('Udayapur', 'Udayapur'),
        ('Sankhuwasabha', 'Sankhuwasabha'),
        # Central Region
        ('Nuwakot', 'Nuwakot'),
        ('Sindhupalchok', 'Sindhupalchok'),
        ('Gorkha', 'Gorkha'),
        ('Lamjung', 'Lamjung'),
        ('Tanahu', 'Tanahu'),
        ('Chitwan', 'Chitwan'),
        ('Nawalpur', 'Nawalpur'),
        ('Parsa', 'Parsa'),
        ('Bara', 'Bara'),
        ('Rautahat', 'Rautahat'),
        # Western Region
        ('Gulmi', 'Gulmi'),
        ('Arghakhanchi', 'Arghakhanchi'),
        ('Palpa', 'Palpa'),
        ('Dang', 'Dang'),
        ('Banke', 'Banke'),
        ('Bardiya', 'Bardiya'),
        ('Surkhet', 'Surkhet'),
        # Mid-Western Region
        ('Salyan', 'Salyan'),
        ('Pyuthan', 'Pyuthan'),
        ('Rolpa', 'Rolpa'),
        ('Rukum', 'Rukum'),
        ('Dailekh', 'Dailekh'),
        ('Jumla', 'Jumla'),
        ('Kalikot', 'Kalikot'),
        ('Dolpa', 'Dolpa'),
        # Far-Western Region
        ('Jajarkot', 'Jajarkot'),
        ('Achham', 'Achham'),
        ('Bajura', 'Bajura'),
        ('Bajhang', 'Bajhang'),
        ('Doti', 'Doti'),
        ('Kailali', 'Kailali'),
        ('Kanchanpur', 'Kanchanpur'),
    ]
    
    hospital_id = models.CharField(max_length=50, unique=True)
    hospital_name = models.CharField(max_length=200)
    district = models.CharField(max_length=100, choices=DISTRICTS, default='Kathmandu')
    blood_type_needed = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    blood_product_needed = models.CharField(max_length=20, choices=BLOOD_PRODUCT_CHOICES, default='whole_blood')
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
    DISTRICTS = [
        # Bagmati Province
        ('Kathmandu', 'Kathmandu'),
        ('Bhaktapur', 'Bhaktapur'),
        ('Lalitpur', 'Lalitpur'),
        ('Kavre', 'Kavre'),
        ('Nuwakot', 'Nuwakot'),
        ('Rasuwa', 'Rasuwa'),
        ('Sindhuli', 'Sindhuli'),
        ('Ramechhap', 'Ramechhap'),
        ('Dolakha', 'Dolakha'),
        ('Makwanpur', 'Makwanpur'),
        # Eastern Region
        ('Ilam', 'Ilam'),
        ('Jhapa', 'Jhapa'),
        ('Morang', 'Morang'),
        ('Sunsari', 'Sunsari'),
        ('Dhankuta', 'Dhankuta'),
        ('Terhathum', 'Terhathum'),
        ('Panchthar', 'Panchthar'),
        ('Udayapur', 'Udayapur'),
        ('Sankhuwasabha', 'Sankhuwasabha'),
        ('Sindhupalchok', 'Sindhupalchok'),
        # Central Region
        ('Gorkha', 'Gorkha'),
        ('Lamjung', 'Lamjung'),
        ('Tanahu', 'Tanahu'),
        ('Chitwan', 'Chitwan'),
        ('Nawalpur', 'Nawalpur'),
        ('Parsa', 'Parsa'),
        ('Bara', 'Bara'),
        ('Rautahat', 'Rautahat'),
        ('Gulmi', 'Gulmi'),
        ('Arghakhanchi', 'Arghakhanchi'),
        # Western Region
        ('Palpa', 'Palpa'),
        ('Dang', 'Dang'),
        ('Banke', 'Banke'),
        ('Bardiya', 'Bardiya'),
        ('Surkhet', 'Surkhet'),
        # Mid-Western Region
        ('Salyan', 'Salyan'),
        ('Pyuthan', 'Pyuthan'),
        ('Rolpa', 'Rolpa'),
        ('Rukum', 'Rukum'),
        ('Dailekh', 'Dailekh'),
        ('Jumla', 'Jumla'),
        ('Kalikot', 'Kalikot'),
        ('Dolpa', 'Dolpa'),
        # Far-Western Region
        ('Jajarkot', 'Jajarkot'),
        ('Achham', 'Achham'),
        ('Bajura', 'Bajura'),
        ('Bajhang', 'Bajhang'),
        ('Doti', 'Doti'),
        ('Kailali', 'Kailali'),
        ('Kanchanpur', 'Kanchanpur'),
    ]
    
    name = models.CharField(max_length=200)
    district = models.CharField(max_length=100, choices=DISTRICTS, default='Kathmandu')
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
    """Legacy medicine rewards model - kept for backward compatibility"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    points_cost = models.IntegerField()
    image = models.ImageField(upload_to='store_items/', null=True, blank=True)
    stock = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Redemption(models.Model):
    """Legacy redemption model - kept for backward compatibility"""
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


# New Reward System with Three Categories

class MoneyReward(models.Model):
    """Points to Money Reward: 1 RS Esewa for every 100 points"""
    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE, related_name='money_rewards')
    points_used = models.IntegerField()
    esewa_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount in RS (1 RS per 100 points)")
    esewa_id = models.CharField(max_length=100, unique=True, help_text="Esewa transaction ID")
    redeemed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ])
    
    class Meta:
        ordering = ['-redeemed_at']
    
    def __str__(self):
        return f"{self.donor.user.username} - {self.esewa_amount} RS ({self.points_used} points)"


class DiscountReward(models.Model):
    """Points to Discounts Reward: Exclusive discounts from restaurants and businesses"""
    name = models.CharField(max_length=200)
    business_name = models.CharField(max_length=200, help_text="Name of restaurant/business offering discount")
    business_type = models.CharField(max_length=100, help_text="e.g., Restaurant, Pharmacy, Grocery Store")
    description = models.TextField(help_text="Description of the discount offered")
    discount_percentage = models.IntegerField(help_text="Discount percentage offered")
    points_cost = models.IntegerField(help_text="Points required to unlock this discount")
    image = models.ImageField(upload_to='discount_rewards/', null=True, blank=True)
    coupon_code = models.CharField(max_length=50, unique=True, help_text="Unique coupon code for this discount")
    valid_until = models.DateField()
    active = models.BooleanField(default=True)
    stock = models.IntegerField(default=-1, help_text="Number of available coupons (-1 for unlimited)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.business_name} ({self.discount_percentage}% off)"


class DiscountRedemption(models.Model):
    """Redemption record for discount rewards"""
    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE, related_name='discount_redemptions')
    discount_reward = models.ForeignKey(DiscountReward, on_delete=models.CASCADE, related_name='redemptions')
    points_used = models.IntegerField()
    redeemed_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True, help_text="When the discount was actually used")
    status = models.CharField(max_length=20, default='active', choices=[
        ('active', 'Active'),
        ('used', 'Used'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ])
    
    class Meta:
        ordering = ['-redeemed_at']
    
    def __str__(self):
        return f"{self.donor.user.username} - {self.discount_reward.business_name} ({self.discount_reward.discount_percentage}%)"


class MedicineReward(models.Model):
    """Points to Medicine Reward: Original medicine/healthcare product rewards"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, help_text="e.g., Medicine, Supplement, Healthcare Item")
    points_cost = models.IntegerField()
    image = models.ImageField(upload_to='medicine_rewards/', null=True, blank=True)
    provider = models.CharField(max_length=200, help_text="Pharmacy/Healthcare provider name")
    stock = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class MedicineRedemption(models.Model):
    """Redemption record for medicine rewards"""
    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE, related_name='medicine_redemptions')
    medicine_reward = models.ForeignKey(MedicineReward, on_delete=models.CASCADE, related_name='redemptions')
    points_used = models.IntegerField()
    redeemed_at = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField(blank=True)
    delivery_phone = models.CharField(max_length=15, blank=True)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('dispatched', 'Dispatched'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ])
    
    class Meta:
        ordering = ['-redeemed_at']
    
    def __str__(self):
        return f"{self.donor.user.username} - {self.medicine_reward.name}"


class Hospital(models.Model):
    """Registered hospital/blood bank that sends automated events."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100, default='Kathmandu')
    address = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    api_key_hash = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hospital"
        verbose_name_plural = "Hospitals"

    def __str__(self):
        return f"{self.name} ({self.code})"


class Transaction(models.Model):
    """Append-only ledger of incoming or outgoing blood units."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='transactions')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    units_change = models.IntegerField(help_text="Positive for donation received, negative for units issued")
    timestamp = models.DateTimeField()
    ingested_at = models.DateTimeField(auto_now_add=True)
    source_reference = models.CharField(max_length=100, blank=True)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-ingested_at']

    def __str__(self):
        return f"{self.hospital.code} {self.blood_group} {self.units_change}"


class BloodStock(models.Model):
    """Materialized current stock per hospital and blood group."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='stock')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    blood_product_type = models.CharField(max_length=20, choices=BLOOD_PRODUCT_CHOICES, default='whole_blood')
    units_available = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('hospital', 'blood_group', 'blood_product_type')
        ordering = ['hospital__name', 'blood_group']

    def __str__(self):
        product_display = dict(BLOOD_PRODUCT_CHOICES).get(self.blood_product_type, self.blood_product_type)
        return f"{self.hospital.code} {self.blood_group} ({product_display}): {self.units_available}"


class StockAlert(models.Model):
    """Track low stock alerts for hospitals."""
    ALERT_LEVELS = [
        ('low', 'Low'),
        ('critical', 'Critical'),
        ('emergency', 'Emergency'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='alerts')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    alert_level = models.CharField(max_length=20, choices=ALERT_LEVELS)
    threshold = models.IntegerField()
    current_units = models.IntegerField()
    triggered_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    notified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-triggered_at']
    
    def __str__(self):
        return f"{self.hospital.code} {self.blood_group} - {self.alert_level}"
    
    @property
    def is_resolved(self):
        return self.resolved_at is not None


class DonationDrive(models.Model):
    """Suggested or planned blood donation campaigns."""
    URGENCY_LEVELS = [
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    blood_groups = models.JSONField(help_text="List of blood groups needed, e.g., ['O+', 'A-']")
    urgency = models.CharField(max_length=20, choices=URGENCY_LEVELS)
    target_units = models.IntegerField()
    collected_units = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    description = models.TextField(blank=True)
    location = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.title} - {self.city}"
    
    @property
    def progress_percentage(self):
        if self.target_units == 0:
            return 0
        return min(100, (self.collected_units / self.target_units) * 100)

