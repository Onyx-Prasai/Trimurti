from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .views import (
    DonorProfileViewSet, HospitalReqViewSet, BloodBankViewSet,
    DonationViewSet, StoreItemViewSet, RedemptionViewSet, AIHealthViewSet,
    HospitalViewSet, TransactionViewSet, TransactionIngestView, StockView,
    BloodRequestViewSet,
)
from .reward_views import (
    MoneyRewardViewSet, DiscountRewardViewSet, DiscountRedemptionViewSet,
    MedicineRewardViewSet, MedicineRedemptionViewSet,
)
from .bloodsync_views import (
    PublicBloodStockView, BloodAvailabilityByCityView, AdminAnalyticsView,
    StockAlertViewSet, DonationDriveViewSet, hospital_list_public,
    check_stock_alerts, blood_stock_map_data, NearbyDonorLocatorView, priority_hospitals,
)

# Blood Group Update Endpoint
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_blood_group(request):
    """Update user's blood group"""
    try:
        from .models import DonorProfile
        
        donor = DonorProfile.objects.get(user=request.user)
        blood_group = request.data.get('blood_group')
        
        if not blood_group:
            return Response({'error': 'Blood group is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        valid_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        if blood_group not in valid_groups:
            return Response({'error': 'Invalid blood group'}, status=status.HTTP_400_BAD_REQUEST)
        
        donor.blood_group = blood_group
        donor.save()
        
        return Response({
            'message': 'Blood group updated successfully',
            'blood_group': blood_group
        }, status=status.HTTP_200_OK)
    
    except DonorProfile.DoesNotExist:
        return Response({'error': 'Donor profile not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

urlpatterns = [
    path('', include(router.urls)),
    
    # Blood Group Update
    path('donor-profile/update-blood-group/', update_blood_group, name='update-blood-group'),
    
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
]


