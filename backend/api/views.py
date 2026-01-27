from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.db import transaction as db_transaction
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import (
    DonorProfile,
    HospitalReq,
    BloodBank,
    Donation,
    StoreItem,
    Redemption,
    Hospital,
    BloodStock,
    Transaction,
)
from .serializers import (
    DonorProfileSerializer, HospitalReqSerializer, BloodBankSerializer,
    DonationSerializer, StoreItemSerializer, RedemptionSerializer,
    HospitalSerializer, BloodStockSerializer, TransactionSerializer,
    IngestTransactionSerializer,
)
from .prediction import predict_blood_needs
from django.conf import settings
import os
from .authentication import HospitalAPIKeyAuthentication


class DonorProfileViewSet(viewsets.ModelViewSet):
    queryset = DonorProfile.objects.all()
    serializer_class = DonorProfileSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get overall platform statistics"""
        total_donors = DonorProfile.objects.count()
        active_donors = DonorProfile.objects.filter(
            last_donation_date__isnull=False
        ).count()
        total_donations = Donation.objects.filter(confirmed=True).count()
        lives_saved = total_donations * 3
        
        return Response({
            'total_donors': total_donors,
            'active_donors': active_donors,
            'total_donations': total_donations,
            'lives_saved': lives_saved,
            'blood_banks': BloodBank.objects.count(),
        })
    
    @action(detail=True, methods=['post'])
    def register_donation(self, request, pk=None):
        """Register a new donation and award points"""
        donor = self.get_object()
        
        if not donor.can_donate():
            return Response({
                'error': f'Cannot donate yet. Wait {donor.days_until_next_donation()} more days.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        hospital_id = request.data.get('hospital_id')
        hospital = None
        if hospital_id:
            try:
                hospital = HospitalReq.objects.get(id=hospital_id)
            except HospitalReq.DoesNotExist:
                pass
        
        donation = Donation.objects.create(
            donor=donor,
            hospital=hospital,
            donation_date=timezone.now().date(),
            confirmed=True
        )
        
        # Update donor profile
        donor.last_donation_date = timezone.now().date()
        donor.total_donations += 1
        donor.points += 100
        donor.save()
        
        # Award referral bonus if applicable
        if donor.referred_by:
            referrer = donor.referred_by
            referrer.points += 20
            referrer.save()
        
        return Response(DonationSerializer(donation).data)


class HospitalReqViewSet(viewsets.ModelViewSet):
    queryset = HospitalReq.objects.filter(fulfilled=False).order_by('-is_critical', '-created_at')
    serializer_class = HospitalReqSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = HospitalReq.objects.filter(fulfilled=False)
        
        # Filter by blood type
        blood_type = self.request.query_params.get('blood_type', None)
        if blood_type:
            queryset = queryset.filter(blood_type_needed=blood_type)
        
        # Filter by city
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city=city)
        
        # Filter by hospital name
        hospital_name = self.request.query_params.get('hospital_name', None)
        if hospital_name:
            queryset = queryset.filter(hospital_name__icontains=hospital_name)
        
        return queryset.order_by('-is_critical', '-created_at')
    
    @action(detail=False, methods=['get'])
    def predictions(self, request):
        """Get predicted blood needs by region"""
        predictions = predict_blood_needs()
        return Response(predictions)


class BloodBankViewSet(viewsets.ModelViewSet):
    queryset = BloodBank.objects.all()
    serializer_class = BloodBankSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = BloodBank.objects.all()
        
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city=city)
        
        return queryset


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [AllowAny]


class StoreItemViewSet(viewsets.ModelViewSet):
    queryset = StoreItem.objects.filter(active=True)
    serializer_class = StoreItemSerializer
    permission_classes = [AllowAny]


class RedemptionViewSet(viewsets.ModelViewSet):
    queryset = Redemption.objects.all()
    serializer_class = RedemptionSerializer
    permission_classes = [AllowAny]
    
    def create(self, request):
        """Redeem points for store item"""
        donor_id = request.data.get('donor_id')
        item_id = request.data.get('item_id')
        
        try:
            donor = DonorProfile.objects.get(id=donor_id)
            item = StoreItem.objects.get(id=item_id)
        except (DonorProfile.DoesNotExist, StoreItem.DoesNotExist):
            return Response({'error': 'Invalid donor or item'}, status=status.HTTP_400_BAD_REQUEST)
        
        if donor.points < item.points_cost:
            return Response({'error': 'Insufficient points'}, status=status.HTTP_400_BAD_REQUEST)
        
        if item.stock <= 0:
            return Response({'error': 'Item out of stock'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create redemption
        redemption = Redemption.objects.create(
            donor=donor,
            item=item,
            points_used=item.points_cost,
            status='completed'
        )
        
        # Deduct points and stock
        donor.points -= item.points_cost
        donor.save()
        item.stock -= 1
        item.save()
        
        return Response(RedemptionSerializer(redemption).data)


class AIHealthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    def _get_model(self):
        """Lazy load Gemini API to avoid import errors at startup"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            return genai.GenerativeModel('gemini-pro')
        except ImportError as e:
            raise ImportError(f"Failed to import google.generativeai: {e}. Please install a compatible version.")
    
    @action(detail=False, methods=['post'])
    def chat(self, request):
        """Chat with AI health assistant"""
        message = request.data.get('message', '')
        
        if not message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            model = self._get_model()
            prompt = f"""You are a health assistant for Blood Hub Nepal. Provide helpful, accurate health information related to blood donation, nutrition, and general wellness. 
            Focus on Nepalese dietary recommendations when relevant. Keep responses concise and practical.
            
            User question: {message}
            
            Response:"""
            
            response = model.generate_content(prompt)
            return Response({'response': response.text})
        except ImportError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Catching potential API errors more gracefully
            error_message = f"An error occurred while communicating with the AI service: {str(e)}"
            # Check for common API key-related errors
            if "API key not valid" in str(e) or "PERMISSION_DENIED" in str(e):
                error_message = "The provided API key is invalid or lacks the necessary permissions. Please check your key and try again."
                return Response({'error': error_message}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HospitalViewSet(viewsets.ReadOnlyModelViewSet):
    """Public registry of participating hospitals."""

    queryset = Hospital.objects.filter(is_active=True)
    serializer_class = HospitalSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Hospital.objects.filter(is_active=True)
        city = self.request.query_params.get('city')
        search = self.request.query_params.get('search')
        if city:
            queryset = queryset.filter(city__icontains=city)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """View-only access to transaction ledger (for demos/ops)."""

    queryset = Transaction.objects.select_related('hospital')
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Transaction.objects.select_related('hospital')
        hospital_id = self.request.query_params.get('hospital_id')
        if hospital_id:
            queryset = queryset.filter(hospital_id=hospital_id)
        blood_group = self.request.query_params.get('blood_group')
        if blood_group:
            queryset = queryset.filter(blood_group=blood_group)
        return queryset


class TransactionIngestView(APIView):
    """Hospital-side ingestion endpoint (API-key protected)."""

    authentication_classes = [HospitalAPIKeyAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = IngestTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hospital = getattr(request, "user", None)
        if not isinstance(hospital, Hospital):
            return Response(
                {"detail": "Valid X-API-Key header is required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        data = serializer.validated_data
        with db_transaction.atomic():
            # Append to transaction ledger
            txn = Transaction.objects.create(
                hospital=hospital,
                blood_group=data['blood_group'],
                units_change=data['units_change'],
                timestamp=data['timestamp'],
                source_reference=data.get('source_reference', ''),
                notes=data.get('notes', ''),
            )

            # Update materialized stock with row-level locking
            stock, _ = BloodStock.objects.select_for_update().get_or_create(
                hospital=hospital,
                blood_group=data['blood_group'],
                defaults={'units_available': 0},
            )
            stock.units_available = max(0, stock.units_available + data['units_change'])
            stock.save()

        return Response(
            {
                "message": "Transaction ingested",
                "transaction": TransactionSerializer(txn).data,
                "stock": BloodStockSerializer(stock).data,
            },
            status=status.HTTP_202_ACCEPTED,
        )


class StockView(APIView):
    """Public stock lookup endpoint."""

    permission_classes = [AllowAny]

    def get(self, request):
        blood_group = request.query_params.get('blood_group')
        city = request.query_params.get('city')

        queryset = BloodStock.objects.select_related('hospital')
        if blood_group:
            queryset = queryset.filter(blood_group=blood_group)
        if city:
            queryset = queryset.filter(hospital__city__icontains=city)

        serializer = BloodStockSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def analyze_report(self, request):
        """Analyze medical report using Gemini Vision"""
        try:
            # For text-based analysis (if image upload is handled separately)
            report_text = request.data.get('report_text', '')
            report_type = request.data.get('report_type', 'general')
            
            if not report_text:
                return Response({'error': 'Report text is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            model = self._get_model()
            prompt = f"""Analyze this medical report and provide specific recommendations:
            
            Report Type: {report_type}
            Report Content: {report_text}
            
            Please provide:
            1. Key findings
            2. Specific Nepalese dietary recommendations (iron-rich foods like spinach, lentils, etc.)
            3. Lifestyle suggestions
            4. When to consult a doctor
            
            Response:"""
            
            response = model.generate_content(prompt)
            return Response({'analysis': response.text})
        except ImportError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Catching potential API errors more gracefully
            error_message = f"An error occurred while communicating with the AI service: {str(e)}"
            # Check for common API key-related errors
            if "API key not valid" in str(e) or "PERMISSION_DENIED" in str(e):
                error_message = "The provided API key is invalid or lacks the necessary permissions. Please check your key and try again."
                return Response({'error': error_message}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

