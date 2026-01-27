from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DonorProfileViewSet, HospitalReqViewSet, BloodBankViewSet,
    DonationViewSet, StoreItemViewSet, RedemptionViewSet, AIHealthViewSet,
    HospitalViewSet, TransactionViewSet, TransactionIngestView, StockView,
)

router = DefaultRouter()
router.register(r'donors', DonorProfileViewSet, basename='donor')
router.register(r'hospitals', HospitalReqViewSet, basename='hospital')
router.register(r'bloodbanks', BloodBankViewSet, basename='bloodbank')
router.register(r'donations', DonationViewSet, basename='donation')
router.register(r'store', StoreItemViewSet, basename='store')
router.register(r'redemptions', RedemptionViewSet, basename='redemption')
router.register(r'ai-health', AIHealthViewSet, basename='ai-health')
router.register(r'hospital-registry', HospitalViewSet, basename='hospital-registry')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('ingest/transactions/', TransactionIngestView.as_view(), name='ingest-transaction'),
    path('stock/', StockView.as_view(), name='stock'),
]

