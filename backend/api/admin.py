from django.contrib import admin
from django.utils.html import format_html
from .models import (
    DonorProfile, HospitalReq, BloodBank, Donation, StoreItem, Redemption,
    Hospital, BloodStock, Transaction
)
from .authentication import hash_api_key
import secrets


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


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    """BloodSync Nepal - Hospital Management"""
    list_display = ['code', 'name', 'city', 'is_active', 'created_at', 'stock_summary']
    list_filter = ['is_active', 'city', 'created_at']
    search_fields = ['code', 'name', 'city']
    readonly_fields = ['id', 'created_at', 'updated_at', 'api_key_hash', 'display_api_key']
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'code', 'name', 'city', 'address')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('API Configuration', {
            'fields': ('api_key_hash', 'display_api_key', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def stock_summary(self, obj):
        """Display total units across all blood groups"""
        total = sum(stock.units_available for stock in obj.stock.all())
        return format_html('<strong>{}</strong> units', total)
    stock_summary.short_description = 'Total Stock'
    
    def display_api_key(self, obj):
        """Show message about API key"""
        if obj.id:
            return "API key is hashed and cannot be displayed. Generate new key if needed."
        return "API key will be generated upon save."
    display_api_key.short_description = 'API Key Info'
    
    def save_model(self, request, obj, form, change):
        """Generate API key for new hospitals"""
        if not change:  # New hospital
            raw_key = secrets.token_urlsafe(32)
            obj.api_key_hash = hash_api_key(raw_key)
            super().save_model(request, obj, form, change)
            # Store key temporarily to display to admin
            request.session['new_hospital_api_key'] = raw_key
            self.message_user(request, f"Hospital created! API Key (save this securely): {raw_key}")
        else:
            super().save_model(request, obj, form, change)


@admin.register(BloodStock)
class BloodStockAdmin(admin.ModelAdmin):
    """BloodSync Nepal - Current Blood Inventory"""
    list_display = ['hospital', 'blood_group', 'units_available', 'stock_status', 'updated_at']
    list_filter = ['blood_group', 'hospital__city', 'updated_at']
    search_fields = ['hospital__name', 'hospital__code']
    readonly_fields = ['id', 'updated_at']
    ordering = ['hospital__name', 'blood_group']
    
    def stock_status(self, obj):
        """Visual indicator for stock levels"""
        if obj.units_available < 5:
            color = 'red'
            status = 'CRITICAL'
        elif obj.units_available < 15:
            color = 'orange'
            status = 'LOW'
        elif obj.units_available < 30:
            color = '#FFA500'
            status = 'MODERATE'
        else:
            color = 'green'
            status = 'GOOD'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, status
        )
    stock_status.short_description = 'Status'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """BloodSync Nepal - Transaction Audit Log"""
    list_display = ['timestamp', 'hospital', 'blood_group', 'units_change_display', 'source_reference', 'ingested_at']
    list_filter = ['hospital__city', 'blood_group', 'timestamp', 'ingested_at']
    search_fields = ['hospital__name', 'hospital__code', 'source_reference', 'notes']
    readonly_fields = ['id', 'ingested_at']
    ordering = ['-ingested_at']
    date_hierarchy = 'timestamp'
    
    def units_change_display(self, obj):
        """Color-coded units change"""
        if obj.units_change > 0:
            color = 'green'
            symbol = '+'
        else:
            color = 'red'
            symbol = ''
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}{}</span>',
            color, symbol, obj.units_change
        )
    units_change_display.short_description = 'Units Change'

