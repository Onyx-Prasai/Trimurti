from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DonorProfileViewSet, HospitalReqViewSet, BloodBankViewSet,
    DonationViewSet, StoreItemViewSet, RedemptionViewSet, AIHealthViewSet,
    HospitalViewSet, TransactionViewSet, TransactionIngestView, StockView,
)
from .bloodsync_views import (
    PublicBloodStockView, BloodAvailabilityByCityView, AdminAnalyticsView,
    StockAlertViewSet, DonationDriveViewSet, hospital_list_public,
    check_stock_alerts, blood_stock_map_data,
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

# BloodSync Nepal specific endpoints
router.register(r'alerts', StockAlertViewSet, basename='alert')
router.register(r'donation-drives', DonationDriveViewSet, basename='donation-drive')

urlpatterns = [
    path('', include(router.urls)),
    
    # Hospital Integration API (Protected)
    path('v1/ingest/transaction/', TransactionIngestView.as_view(), name='ingest-transaction'),
    
    # Public Query API
    path('v1/public/blood-stock/', PublicBloodStockView.as_view(), name='public-blood-stock'),
    path('v1/public/blood-availability/<str:city>/', BloodAvailabilityByCityView.as_view(), name='blood-availability-city'),
    path('v1/public/hospitals/', hospital_list_public, name='public-hospitals'),
    path('v1/public/map-data/', blood_stock_map_data, name='map-data'),
    
    # Admin API (Protected)
    path('v1/admin/analytics/national/', AdminAnalyticsView.as_view(), name='admin-analytics'),
    path('v1/admin/check-alerts/', check_stock_alerts, name='check-alerts'),
    
    # Legacy endpoints
    path('ingest/transactions/', TransactionIngestView.as_view(), name='ingest-transaction-legacy'),
    path('stock/', StockView.as_view(), name='stock'),
]

