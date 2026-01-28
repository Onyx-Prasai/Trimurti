from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db import transaction as db_transaction
from urllib.parse import urlparse, parse_qs
import logging

logger = logging.getLogger(__name__)

from .models import (
    User,
    HospitalProfile,
    BloodBankProfile,
    AdminProfile,
)
from api.models import DonorProfile
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    HospitalProfileSerializer,
    BloodBankProfileSerializer,
    AdminProfileSerializer,
)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    API endpoint for user login
    """
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'detail': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    API endpoint for user registration
    """
    logger.debug(f"Registration request data: {request.data}")
    serializer = UserRegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        # Create a profile based on user_type
        if user.user_type == 'base_user':
            from api.models import DonorProfile
            donor_profile, created = DonorProfile.objects.get_or_create(user=user)
            
            # Handle referral code (accept raw code or full referral link)
            referral_code = request.data.get('referral_code')
            if referral_code:
                referral_code = str(referral_code).strip()
                if 'ref=' in referral_code or 'referral_code=' in referral_code:
                    try:
                        parsed = urlparse(referral_code)
                        params = parse_qs(parsed.query)
                        referral_code = (params.get('ref') or params.get('referral_code') or [referral_code])[0]
                    except Exception:
                        referral_code = referral_code
                try:
                    referrer = DonorProfile.objects.get(referral_code=referral_code)
                    if referrer != donor_profile:
                        with db_transaction.atomic():
                            donor_profile.referred_by = referrer
                            donor_profile.points += 100
                            referrer.points += 100
                            referrer.save()
                            donor_profile.save()
                        logger.info(f"User {user.username} referred by {referrer.user.username}")
                except DonorProfile.DoesNotExist:
                    logger.warning(f"Invalid referral code: {referral_code}")
            
            # Update phone number if provided (only if not already set)
            if user.phone_number and not donor_profile.phone:
                donor_profile.phone = user.phone_number
            
            donor_profile.save()
        elif user.user_type == 'hospital':
            HospitalProfile.objects.get_or_create(
                user=user,
                defaults={
                    'hospital_name': user.first_name or user.username,
                    'email': user.email,
                    'phone': user.phone_number or '',
                    'address': 'Default Address',
                    'registration_number': f'REG-{user.username}'
                }
            )
        elif user.user_type == 'bloodbank':
            BloodBankProfile.objects.get_or_create(
                user=user,
                defaults={
                    'bank_name': user.first_name or user.username,
                    'email': user.email,
                    'phone': user.phone_number or '',
                    'address': 'Default Address',
                    'registration_number': f'REG-{user.username}'
                }
            )
        elif user.user_type == 'admin':
            AdminProfile.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    
    logger.error(f"Registration errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    User ViewSet for CRUD operations
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'register']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Get current user info
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """
        Filter users by type
        """
        user_type = request.query_params.get('type')

        if user_type:
            users = User.objects.filter(user_type=user_type)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)

        return Response(
            {"error": "type parameter required"},
            status=status.HTTP_400_BAD_REQUEST
        )


class HospitalProfileViewSet(viewsets.ModelViewSet):
    """
    Hospital Profile ViewSet
    """
    queryset = HospitalProfile.objects.all()
    serializer_class = HospitalProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'hospital':
            return HospitalProfile.objects.filter(user=self.request.user)
        return HospitalProfile.objects.all()


class BloodBankProfileViewSet(viewsets.ModelViewSet):
    """
    Blood Bank Profile ViewSet
    """
    queryset = BloodBankProfile.objects.all()
    serializer_class = BloodBankProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'bloodbank':
            return BloodBankProfile.objects.filter(user=self.request.user)
        return BloodBankProfile.objects.all()


class AdminProfileViewSet(viewsets.ModelViewSet):
    """
    Admin Profile ViewSet
    """
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'admin':
            return AdminProfile.objects.filter(user=self.request.user)
        return AdminProfile.objects.all()


