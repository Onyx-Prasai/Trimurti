from rest_framework import serializers
from django.contrib.auth.models import User
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
)


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
        fields = ['id', 'hospital', 'blood_group', 'units_available', 'updated_at']


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


