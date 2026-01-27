from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, HospitalProfile, BloodBankProfile, AdminProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'location', 'profile_picture')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('User Type', {'fields': ('user_type', 'is_verified')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'user_type', 'is_verified', 'is_staff')
    list_filter = ('user_type', 'is_verified', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(HospitalProfile)
class HospitalProfileAdmin(admin.ModelAdmin):
    list_display = ('hospital_name', 'user', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('hospital_name', 'registration_number', 'user__username')


@admin.register(BloodBankProfile)
class BloodBankProfileAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'user', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('bank_name', 'registration_number', 'user__username')


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'access_level', 'created_at')
    list_filter = ('access_level', 'created_at')
    search_fields = ('user__username', 'department')
