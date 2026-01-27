from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db import transaction as db_transaction
from django.utils import timezone
from datetime import date

from .models import (
    DonorProfile,
    MoneyReward,
    DiscountReward,
    DiscountRedemption,
    MedicineReward,
    MedicineRedemption,
)
from .serializers import (
    MoneyRewardSerializer,
    DiscountRewardSerializer,
    DiscountRedemptionSerializer,
    MedicineRewardSerializer,
    MedicineRedemptionSerializer,
)


class MoneyRewardViewSet(viewsets.ModelViewSet):
    """ViewSet for Money Rewards (Points to Esewa conversion)"""
    queryset = MoneyReward.objects.all()
    serializer_class = MoneyRewardSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active money rewards"""
        rewards = self.queryset.filter(status='pending').order_by('-redeemed_at')
        serializer = self.get_serializer(rewards, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def redeem(self, request):
        """Redeem points for Esewa money"""
        donor_id = request.data.get('donor_id')
        points_to_redeem = request.data.get('points')
        
        if not donor_id or not points_to_redeem:
            return Response({'error': 'donor_id and points are required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            donor = DonorProfile.objects.get(id=donor_id)
        except DonorProfile.DoesNotExist:
            return Response({'error': 'Donor not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if donor.points < points_to_redeem:
            return Response({'error': 'Insufficient points'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 100 points = 1 RS
        esewa_amount = points_to_redeem / 100
        
        with db_transaction.atomic():
            reward = MoneyReward.objects.create(
                donor=donor,
                points_used=points_to_redeem,
                esewa_amount=esewa_amount,
                esewa_id=f"ESW-{donor_id}-{timezone.now().timestamp()}",
                status='completed'
            )
            
            donor.points -= points_to_redeem
            donor.save()
        
        serializer = self.get_serializer(reward)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DiscountRewardViewSet(viewsets.ModelViewSet):
    """ViewSet for Discount Rewards"""
    queryset = DiscountReward.objects.filter(active=True).order_by('-created_at')
    serializer_class = DiscountRewardSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available discount rewards"""
        rewards = self.queryset.filter(valid_until__gte=date.today())
        serializer = self.get_serializer(rewards, many=True)
        return Response(serializer.data)


class DiscountRedemptionViewSet(viewsets.ModelViewSet):
    """ViewSet for Discount Redemptions"""
    queryset = DiscountRedemption.objects.all().order_by('-redeemed_at')
    serializer_class = DiscountRedemptionSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def redeem(self, request):
        """Redeem a discount reward"""
        donor_id = request.data.get('donor_id')
        discount_reward_id = request.data.get('discount_reward_id')
        
        if not donor_id or not discount_reward_id:
            return Response({'error': 'donor_id and discount_reward_id are required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            donor = DonorProfile.objects.get(id=donor_id)
            discount_reward = DiscountReward.objects.get(id=discount_reward_id)
        except (DonorProfile.DoesNotExist, DiscountReward.DoesNotExist):
            return Response({'error': 'Donor or discount reward not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        if donor.points < discount_reward.points_cost:
            return Response({'error': 'Insufficient points'}, status=status.HTTP_400_BAD_REQUEST)
        
        if discount_reward.stock > 0:
            discount_reward.stock -= 1
            discount_reward.save()
        
        with db_transaction.atomic():
            redemption = DiscountRedemption.objects.create(
                donor=donor,
                discount_reward=discount_reward,
                points_used=discount_reward.points_cost,
                status='active'
            )
            
            donor.points -= discount_reward.points_cost
            donor.save()
        
        serializer = self.get_serializer(redemption)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def mark_used(self, request, pk=None):
        """Mark a discount as used"""
        redemption = self.get_object()
        redemption.status = 'used'
        redemption.used_at = timezone.now()
        redemption.save()
        
        serializer = self.get_serializer(redemption)
        return Response(serializer.data)


class MedicineRewardViewSet(viewsets.ModelViewSet):
    """ViewSet for Medicine Rewards"""
    queryset = MedicineReward.objects.filter(active=True).order_by('-created_at')
    serializer_class = MedicineRewardSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available medicine rewards"""
        rewards = self.queryset.filter(stock__gt=0)
        serializer = self.get_serializer(rewards, many=True)
        return Response(serializer.data)


class MedicineRedemptionViewSet(viewsets.ModelViewSet):
    """ViewSet for Medicine Redemptions"""
    queryset = MedicineRedemption.objects.all().order_by('-redeemed_at')
    serializer_class = MedicineRedemptionSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def redeem(self, request):
        """Redeem a medicine reward"""
        donor_id = request.data.get('donor_id')
        medicine_reward_id = request.data.get('medicine_reward_id')
        delivery_address = request.data.get('delivery_address', '')
        delivery_phone = request.data.get('delivery_phone', '')
        
        if not donor_id or not medicine_reward_id:
            return Response({'error': 'donor_id and medicine_reward_id are required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            donor = DonorProfile.objects.get(id=donor_id)
            medicine_reward = MedicineReward.objects.get(id=medicine_reward_id)
        except (DonorProfile.DoesNotExist, MedicineReward.DoesNotExist):
            return Response({'error': 'Donor or medicine reward not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        if donor.points < medicine_reward.points_cost:
            return Response({'error': 'Insufficient points'}, status=status.HTTP_400_BAD_REQUEST)
        
        if medicine_reward.stock <= 0:
            return Response({'error': 'Out of stock'}, status=status.HTTP_400_BAD_REQUEST)
        
        with db_transaction.atomic():
            redemption = MedicineRedemption.objects.create(
                donor=donor,
                medicine_reward=medicine_reward,
                points_used=medicine_reward.points_cost,
                delivery_address=delivery_address,
                delivery_phone=delivery_phone,
                status='pending'
            )
            
            donor.points -= medicine_reward.points_cost
            donor.save()
            
            medicine_reward.stock -= 1
            medicine_reward.save()
        
        serializer = self.get_serializer(redemption)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
