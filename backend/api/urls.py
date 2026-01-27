from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DonorProfileViewSet, HospitalReqViewSet, BloodBankViewSet,
    DonationViewSet, StoreItemViewSet, RedemptionViewSet, AIHealthViewSet
)

router = DefaultRouter()
router.register(r'donors', DonorProfileViewSet, basename='donor')
router.register(r'hospitals', HospitalReqViewSet, basename='hospital')
router.register(r'bloodbanks', BloodBankViewSet, basename='bloodbank')
router.register(r'donations', DonationViewSet, basename='donation')
router.register(r'store', StoreItemViewSet, basename='store')
router.register(r'redemptions', RedemptionViewSet, basename='redemption')
router.register(r'ai-health', AIHealthViewSet, basename='ai-health')

urlpatterns = [
    path('', include(router.urls)),
]

