from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DonorProfileViewSet, HospitalReqViewSet, BloodBankViewSet,
    DonationViewSet, StoreItemViewSet, RedemptionViewSet, AIHealthViewSet,
    HospitalViewSet, TransactionViewSet, TransactionIngestView, StockView,
)
from .reward_views import (
    MoneyRewardViewSet, DiscountRewardViewSet, DiscountRedemptionViewSet,
    MedicineRewardViewSet, MedicineRedemptionViewSet,
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

urlpatterns = [
    path('', include(router.urls)),
    path('ingest/transactions/', TransactionIngestView.as_view(), name='ingest-transaction'),
    path('stock/', StockView.as_view(), name='stock'),
]


