from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DonorProfileViewSet, HospitalReqViewSet, BloodBankViewSet,
    DonationViewSet, StoreItemViewSet, RedemptionViewSet, AIHealthViewSet,
    HospitalViewSet, TransactionViewSet, TransactionIngestView, StockView,
    BloodRequestViewSet,
)
from .sms_views import SMSViewSet, SMSAPIView
from .reward_views import (
    MoneyRewardViewSet, DiscountRewardViewSet, DiscountRedemptionViewSet,
    MedicineRewardViewSet, MedicineRedemptionViewSet,
)
from .bloodsync_views import (
    PublicBloodStockView, BloodAvailabilityByCityView, AdminAnalyticsView,
    StockAlertViewSet, DonationDriveViewSet, hospital_list_public,
    check_stock_alerts, blood_stock_map_data, NearbyDonorLocatorView, priority_hospitals,
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
# New Reward System Routes
router.register(r'rewards/money', MoneyRewardViewSet, basename='money-reward')
router.register(r'rewards/discounts', DiscountRewardViewSet, basename='discount-reward')
router.register(r'rewards/discount-redemptions', DiscountRedemptionViewSet, basename='discount-redemption')
router.register(r'rewards/medicine', MedicineRewardViewSet, basename='medicine-reward')
router.register(r'rewards/medicine-redemptions', MedicineRedemptionViewSet, basename='medicine-redemption')

# BloodSync Nepal specific endpoints
router.register(r'alerts', StockAlertViewSet, basename='alert')
router.register(r'donation-drives', DonationDriveViewSet, basename='donation-drive')
router.register(r'blood-requests', BloodRequestViewSet, basename='blood-request')

# SMS endpoints
router.register(r'sms', SMSViewSet, basename='sms')

urlpatterns = [
    path('', include(router.urls)),
    
    # Hospital Integration API (Protected)
    path('v1/ingest/transaction/', TransactionIngestView.as_view(), name='ingest-transaction'),
    
    # Public Query API
    path('v1/public/blood-stock/', PublicBloodStockView.as_view(), name='public-blood-stock'),
    path('v1/public/blood-availability/<str:city>/', BloodAvailabilityByCityView.as_view(), name='blood-availability-city'),
    path('v1/public/hospitals/', hospital_list_public, name='public-hospitals'),
    path('v1/public/priority-hospitals/', priority_hospitals, name='priority-hospitals'),
    path('v1/public/map-data/', blood_stock_map_data, name='map-data'),
    
    # Admin API (Protected)
    path('v1/admin/analytics/national/', AdminAnalyticsView.as_view(), name='admin-analytics'),
    path('v1/admin/check-alerts/', check_stock_alerts, name='check-alerts'),
    path('v1/admin/locate-donors/', NearbyDonorLocatorView.as_view(), name='locate-donors'),
    
    # Legacy endpoints
    path('ingest/transactions/', TransactionIngestView.as_view(), name='ingest-transaction-legacy'),
    path('stock/', StockView.as_view(), name='stock'),
    
    # SMS direct endpoint
    path('sms/send/', SMSAPIView.as_view(), name='sms-send'),
]


