from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    DonorProfile,
    HospitalReq,
    BloodBank,
    Donation,
    StoreItem,
    Redemption,
    Hospital,
    BloodStock,
    Transaction,
    StockAlert,
    DonationDrive,
    BLOOD_GROUP_CHOICES,
    BLOOD_PRODUCT_CHOICES,
    MoneyReward,
    DiscountReward,
    DiscountRedemption,
    MedicineReward,
    MedicineRedemption,
        BloodRequest,
        SMSNotificationLog,
    )

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class DonorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    can_donate = serializers.SerializerMethodField()
    days_until_next = serializers.SerializerMethodField()
    lives_saved = serializers.SerializerMethodField()
    badges = serializers.SerializerMethodField()
    
    class Meta:
        model = DonorProfile
        fields = '__all__'
    
    def get_can_donate(self, obj):
        return obj.can_donate()
    
    def get_days_until_next(self, obj):
        return obj.days_until_next_donation()
    
    def get_lives_saved(self, obj):
        return obj.lives_saved()
    
    def get_badges(self, obj):
        return obj.get_badges()


class HospitalReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalReq
        fields = '__all__'


class BloodBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodBank
        fields = '__all__'


class DonationSerializer(serializers.ModelSerializer):
    donor = DonorProfileSerializer(read_only=True)
    hospital = HospitalReqSerializer(read_only=True)
    
    class Meta:
        model = Donation
        fields = '__all__'


class StoreItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreItem
        fields = '__all__'


class RedemptionSerializer(serializers.ModelSerializer):
    donor = DonorProfileSerializer(read_only=True)
    item = StoreItemSerializer(read_only=True)
    
    class Meta:
        model = Redemption
        fields = '__all__'


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = [
            'id',
            'code',
            'name',
            'city',
            'address',
            'latitude',
            'longitude',
            'is_active',
        ]


class BloodStockSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer(read_only=True)

    class Meta:
        model = BloodStock
        fields = ['id', 'hospital', 'blood_group', 'blood_product_type', 'units_available', 'updated_at']


class TransactionSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id',
            'hospital',
            'blood_group',
            'units_change',
            'timestamp',
            'ingested_at',
            'source_reference',
            'notes',
        ]


class IngestTransactionSerializer(serializers.Serializer):
    blood_group = serializers.ChoiceField(choices=BLOOD_GROUP_CHOICES)
    units_change = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
    source_reference = serializers.CharField(required=False, allow_blank=True, max_length=100)
    notes = serializers.CharField(required=False, allow_blank=True, max_length=255)


# New Reward System Serializers

class MoneyRewardSerializer(serializers.ModelSerializer):
    donor_name = serializers.CharField(source='donor.user.username', read_only=True)
    
    class Meta:
        model = MoneyReward
        fields = ['id', 'donor', 'donor_name', 'points_used', 'esewa_amount', 'esewa_id', 
                  'redeemed_at', 'status']
        read_only_fields = ['id', 'redeemed_at']


class DiscountRewardSerializer(serializers.ModelSerializer):
    days_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = DiscountReward
        fields = ['id', 'name', 'business_name', 'business_type', 'description', 
                  'discount_percentage', 'points_cost', 'image', 'coupon_code', 
                  'valid_until', 'days_remaining', 'active', 'stock', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_days_remaining(self, obj):
        from datetime import date
        remaining = (obj.valid_until - date.today()).days
        return max(0, remaining)


class DiscountRedemptionSerializer(serializers.ModelSerializer):
    donor_name = serializers.CharField(source='donor.user.username', read_only=True)
    discount_info = DiscountRewardSerializer(source='discount_reward', read_only=True)
    
    class Meta:
        model = DiscountRedemption
        fields = ['id', 'donor', 'donor_name', 'discount_reward', 'discount_info', 
                  'points_used', 'redeemed_at', 'used_at', 'status']
        read_only_fields = ['id', 'redeemed_at']


class MedicineRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineReward
        fields = ['id', 'name', 'description', 'category', 'points_cost', 'image', 
                  'provider', 'stock', 'active', 'created_at']
        read_only_fields = ['id', 'created_at']


class MedicineRedemptionSerializer(serializers.ModelSerializer):
    donor_name = serializers.CharField(source='donor.user.username', read_only=True)
    medicine_info = MedicineRewardSerializer(source='medicine_reward', read_only=True)
    
    class Meta:
        model = MedicineRedemption
        fields = ['id', 'donor', 'donor_name', 'medicine_reward', 'medicine_info', 
                  'points_used', 'redeemed_at', 'delivery_address', 'delivery_phone', 'status']
        read_only_fields = ['id', 'redeemed_at']


class StockAlertSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer(read_only=True)
    is_resolved = serializers.ReadOnlyField()
    
    class Meta:
        model = StockAlert
        fields = '__all__'


class DonationDriveSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = DonationDrive
        fields = '__all__'


class PublicBloodStockSerializer(serializers.Serializer):
    """Serializer for public blood stock query results."""
    hospital = HospitalSerializer()
    stock = serializers.DictField()
    last_updated = serializers.DateTimeField()

class NearbyDonorRequestSerializer(serializers.Serializer):
    """Validate donor locator requests with radius logic."""
    hospital_id = serializers.UUIDField(required=False)
    hospital_code = serializers.CharField(required=False, max_length=50)
    blood_group = serializers.ChoiceField(choices=BLOOD_GROUP_CHOICES)
    blood_product = serializers.ChoiceField(choices=BLOOD_PRODUCT_CHOICES, default='whole_blood')
    is_critical = serializers.BooleanField(default=False)
    max_radius_km = serializers.FloatField(default=20.0, min_value=0.5, max_value=50.0)
    radius_step_km = serializers.FloatField(default=1.0, min_value=0.1, max_value=10.0)
    min_donor_count = serializers.IntegerField(default=1, min_value=1)
    limit_cities = serializers.ListField(
        child=serializers.CharField(max_length=100), required=False, allow_empty=True
    )

    def validate(self, attrs):
        if not attrs.get('hospital_id') and not attrs.get('hospital_code'):
            raise serializers.ValidationError('Provide either hospital_id or hospital_code')
        return attrs

class SMSNotificationLogSerializer(serializers.ModelSerializer):
    """Serializer for SMS notification logs"""
    class Meta:
        model = SMSNotificationLog
        fields = ['id', 'blood_request', 'recipient', 'phone_number', 'message', 'status', 'sent_at', 'twilio_sid', 'error_message']
        read_only_fields = ['id', 'sent_at', 'twilio_sid', 'error_message']

class BloodRequestSerializer(serializers.ModelSerializer):
    """Serializer for blood requests"""
    created_by_name = serializers.SerializerMethodField()
    sms_logs = SMSNotificationLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = BloodRequest
        fields = [
            'id', 'hospital_name', 'district', 'city', 'location', 'latitude', 'longitude',
            'blood_type', 'blood_product', 'urgency', 'units_needed', 'contact_number',
            'contact_person', 'status', 'created_by', 'created_by_name',
            'created_at', 'updated_at', 'sms_logs'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at', 'sms_logs']
    
    def get_created_by_name(self, obj):
        """Return the name of the user who created the request"""
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip() or obj.created_by.username
        return "Anonymous"


