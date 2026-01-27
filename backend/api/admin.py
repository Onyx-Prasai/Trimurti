from django.contrib import admin
from .models import DonorProfile, HospitalReq, BloodBank, Donation, StoreItem, Redemption


@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'blood_group', 'points', 'total_donations', 'district']
    list_filter = ['blood_group', 'district']
    search_fields = ['user__username', 'user__email']


@admin.register(HospitalReq)
class HospitalReqAdmin(admin.ModelAdmin):
    list_display = ['hospital_name', 'district', 'blood_type_needed', 'is_critical', 'fulfilled']
    list_filter = ['district', 'blood_type_needed', 'is_critical', 'fulfilled']
    search_fields = ['hospital_name']


@admin.register(BloodBank)
class BloodBankAdmin(admin.ModelAdmin):
    list_display = ['name', 'district', 'phone']
    list_filter = ['district']
    search_fields = ['name']


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor', 'donation_date', 'points_awarded', 'confirmed']
    list_filter = ['confirmed', 'donation_date']
    search_fields = ['donor__user__username']


@admin.register(StoreItem)
class StoreItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'points_cost', 'stock', 'active']
    list_filter = ['active']
    search_fields = ['name']


@admin.register(Redemption)
class RedemptionAdmin(admin.ModelAdmin):
    list_display = ['donor', 'item', 'points_used', 'status', 'redeemed_at']
    list_filter = ['status', 'redeemed_at']
    search_fields = ['donor__user__username', 'item__name']

