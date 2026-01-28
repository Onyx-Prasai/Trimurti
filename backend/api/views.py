from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from django.db import transaction as db_transaction
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import timedelta
import base64
from io import BytesIO
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
    StockAlert,
    DonationDrive,
    BloodRequest,
    SMSNotificationLog,
)
from .serializers import (
    DonorProfileSerializer, HospitalReqSerializer, BloodBankSerializer,
    DonationSerializer, StoreItemSerializer, RedemptionSerializer,
    HospitalSerializer, BloodStockSerializer, TransactionSerializer,
    IngestTransactionSerializer, StockAlertSerializer, DonationDriveSerializer,
    PublicBloodStockSerializer, BloodRequestSerializer,
)
from .sms_service import send_blood_request_sms
from .prediction import predict_blood_needs
from django.conf import settings
import os
from .authentication import HospitalAPIKeyAuthentication


class DonorProfileViewSet(viewsets.ModelViewSet):
    queryset = DonorProfile.objects.all()
    serializer_class = DonorProfileSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        """
        Override get_object to allow fetching by user_id
        If pk looks like a user_id, try to get the DonorProfile for that user
        """
        pk = self.kwargs.get('pk')
        try:
            # Try to get by DonorProfile ID first
            return DonorProfile.objects.get(pk=pk)
        except DonorProfile.DoesNotExist:
            # If not found, try to get by user_id
            try:
                return DonorProfile.objects.get(user_id=pk)
            except DonorProfile.DoesNotExist:
                from rest_framework.exceptions import NotFound
                raise NotFound(f'No DonorProfile found for ID or User ID {pk}')
    
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
        
        class BloodRequestViewSet(viewsets.ModelViewSet):
            """ViewSet for managing blood requests and triggering SMS notifications"""
            queryset = BloodRequest.objects.all().order_by('-created_at')
            serializer_class = BloodRequestSerializer
            permission_classes = [AllowAny]
            filterset_fields = ['district', 'city', 'blood_type', 'urgency', 'status']
            search_fields = ['hospital_name', 'location', 'contact_person']
            ordering_fields = ['created_at', 'urgency', 'units_needed']
            ordering = ['-created_at']
    
            def perform_create(self, serializer):
                """
                Override create to set created_by user and trigger SMS notifications
                """
                blood_request = serializer.save(created_by=self.request.user)
                # Trigger SMS notifications to nearby donors
                self.send_sms_notifications(blood_request)
                return blood_request
    
            def send_sms_notifications(self, blood_request):
                """
                Find nearby donors with matching blood type and send SMS notifications
                """
                from .sms_service import send_bulk_blood_request_sms
                from .models import DonorProfile, SMSNotificationLog
        
                # Find donors in the same district with matching blood type
                nearby_donors = DonorProfile.objects.filter(
                    district=blood_request.district,
                    blood_group=blood_request.blood_type,
                ).select_related('user')
        
                if not nearby_donors.exists():
                    return
        
                # Prepare donor list with phone numbers
                donor_data = []
                for donor in nearby_donors:
                    if donor.phone_number:
                        donor_data.append({
                            'phone_number': donor.phone_number,
                            'user': donor.user,
                        })
        
                if not donor_data:
                    return
        
                # Send SMS notifications
                result = send_bulk_blood_request_sms(
                    donors=donor_data,
                    blood_type=blood_request.blood_type,
                    location=f"{blood_request.city}, {blood_request.district}",
                    urgency=blood_request.urgency,
                    blood_request=blood_request
                )
    
            @action(detail=True, methods=['post'])
            def mark_fulfilled(self, request, pk=None):
                """Mark a blood request as fulfilled"""
                blood_request = self.get_object()
                blood_request.status = 'fulfilled'
                blood_request.save()
                serializer = self.get_serializer(blood_request)
                return Response(serializer.data)
    
            @action(detail=True, methods=['post'])
            def mark_cancelled(self, request, pk=None):
                """Mark a blood request as cancelled"""
                blood_request = self.get_object()
                blood_request.status = 'cancelled'
                blood_request.save()
                serializer = self.get_serializer(blood_request)
                return Response(serializer.data)
    
            @action(detail=False, methods=['get'])
            def by_district(self, request):
                """Get blood requests grouped by district"""
                district = request.query_params.get('district')
                if not district:
                    return Response({'error': 'district parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
                requests = BloodRequest.objects.filter(district=district, status='active')
                serializer = self.get_serializer(requests, many=True)
                return Response(serializer.data)
    
            @action(detail=False, methods=['get'])
            def nearby(self, request):
                """Get nearby blood requests for a specific location"""
                district = request.query_params.get('district')
                city = request.query_params.get('city')
        
                requests = BloodRequest.objects.filter(status='active')
                if district:
                    requests = requests.filter(district=district)
                if city:
                    requests = requests.filter(city=city)
        
                serializer = self.get_serializer(requests, many=True)
                return Response(serializer.data)
    
            @action(detail=False, methods=['get'])
            def stats(self, request):
                """Get blood request statistics"""
                total = BloodRequest.objects.count()
                active = BloodRequest.objects.filter(status='active').count()
                fulfilled = BloodRequest.objects.filter(status='fulfilled').count()
        
                # Count by blood type
                from django.db.models import Count
                by_blood_type = BloodRequest.objects.filter(status='active').values('blood_type').annotate(count=Count('id'))
        
                # Count by urgency
                by_urgency = BloodRequest.objects.filter(status='active').values('urgency').annotate(count=Count('id'))
        
                return Response({
                    'total': total,
                    'active': active,
                    'fulfilled': fulfilled,
                    'cancelled': BloodRequest.objects.filter(status='cancelled').count(),
                    'by_blood_type': list(by_blood_type),
                    'by_urgency': list(by_urgency),
                })
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
        
        # Filter by blood product
        blood_product = self.request.query_params.get('blood_product', None)
        if blood_product:
            queryset = queryset.filter(blood_product_needed=blood_product)
        
        # Filter by district (city parameter for backwards compatibility)
        district = self.request.query_params.get('city', None)
        if district:
            queryset = queryset.filter(district=district)
        
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
    
    def _get_client(self):
        """Initialize Mistral AI client"""
        try:
            from mistralai import Mistral
            return Mistral(api_key=settings.MISTRAL_API_KEY)
        except ImportError as e:
            raise ImportError(f"Failed to import mistralai: {e}. Please install mistralai package.")
    
    @action(detail=False, methods=['post'])
    def chat(self, request):
        """Chat with AI health assistant"""
        message = request.data.get('message', '')
        
        if not message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if not settings.MISTRAL_API_KEY:
                return Response({'error': 'Mistral API key is not configured in settings.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            client = self._get_client()
            
            prompt = f"""You are a helpful health and nutrition assistant for Blood Hub Nepal. Your role is to:
1. Provide health tips and wellness advice
2. Recommend nutritious foods and dietary suggestions
3. Offer lifestyle and exercise recommendations
4. Answer blood donation-related questions

IMPORTANT RULES:
- NEVER recommend or mention any medicines, medications, drugs, or pharmaceutical products
- Only suggest natural foods, healthy lifestyle changes, and general wellness advice
- Keep responses concise, practical, and relevant to Nepalese dietary context
- For iron-rich foods, mention: spinach, lentils, red meat, fortified grains, dates
- For calcium-rich foods, mention: milk, yogurt, sesame seeds, leafy greens
- For protein sources, mention: chickpeas, beans, fish, eggs, nuts

User Question: {message}

Provide a helpful, practical answer focused on food and lifestyle. Do not recommend medicines."""
            
            response = client.chat.complete(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": prompt}]
            )
            
            return Response({'response': response.choices[0].message.content})
        except ImportError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            error_message = f"An error occurred while communicating with the AI service: {str(e)}"
            if "unauthorized" in str(e).lower() or "api key" in str(e).lower():
                error_message = "The provided Mistral API key is invalid or unauthorized. Please check your API key configuration and ensure it has the necessary permissions."
                return Response({'error': error_message}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def analyze_image(self, request):
        """Analyze blood report images/PDFs and provide health/dietary recommendations"""
        try:
            # Check if file is provided
            if 'image' not in request.FILES:
                return Response({'error': 'Image or PDF file is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            uploaded_file = request.FILES['image']
            
            # Validate file size (max 5MB)
            if uploaded_file.size > 5 * 1024 * 1024:
                return Response({'error': 'File size must be less than 5MB'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate file type
            allowed_image_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            allowed_document_types = ['application/pdf']
            
            if uploaded_file.content_type not in allowed_image_types + allowed_document_types:
                return Response({'error': f'Invalid file type. Allowed: {", ".join(allowed_image_types + allowed_document_types)}'}, status=status.HTTP_400_BAD_REQUEST)
            
            if uploaded_file.content_type == 'application/pdf':
                # Process PDF using Mistral AI
                if not settings.MISTRAL_API_KEY:
                    return Response({'error': 'Mistral API key is not configured in settings for PDF analysis. Please set MISTRAL_API_KEY.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                try:
                    # Use BytesIO to read the PDF file from memory
                    pdf_file = BytesIO(uploaded_file.read())
                    reader = PdfReader(pdf_file)
                    pdf_text = ""
                    for page in reader.pages:
                        pdf_text += page.extract_text() + "\n"
                    
                    if not pdf_text.strip():
                        return Response({'error': 'Could not extract text from PDF. The PDF might be image-based or encrypted.'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    mistral_client = self._get_client()
                    
                    prompt = f"""You are a health and nutrition advisor for Blood Hub Nepal. Analyze this blood report (extracted from a PDF) and provide:

IMPORTANT RULES:
- NEVER recommend medicines, medications, drugs, or pharmaceutical products
- Only suggest natural foods and lifestyle changes
- Always advise consulting a doctor for medical treatment
- Focus on preventive health and nutrition through diet

ANALYSIS FORMAT:
1. **Health Issues Identified**: List any health concerns visible in the report
2. **Foods to Eat**: Recommend specific Nepalese foods with nutrients they provide:
   - Iron-rich: spinach, lentils, red meat, fortified grains, dates
   - Calcium-rich: milk, yogurt, sesame seeds, leafy greens
   - Protein: chickpeas, beans, fish, eggs, nuts
3. **Foods to Avoid**: List foods that may worsen the identified conditions
4. **Daily Lifestyle Tips**: Exercise and habit recommendations
5. **Additional Wellness Advice**: Other preventive health measures

Blood Report Content:
{pdf_text}

Be specific, practical, and actionable."""
                    
                    response = mistral_client.chat.complete(
                        model="mistral-small-latest",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    return Response({
                        'analysis': response.choices[0].message.content,
                        'status': 'success'
                    })
                except ImportError as e:
                    return Response({'error': f"Missing dependency for PDF processing: {e}. Please install pypdf in your backend environment."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except Exception as pdf_error:
                    return Response({'error': f"Error processing PDF with Mistral AI: {str(pdf_error)}. Ensure pypdf is installed and the PDF is valid, and your Mistral API key is correct."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            elif uploaded_file.content_type in allowed_image_types:
                # Process Image using Mistral AI
                if not settings.MISTRAL_API_KEY:
                    return Response({'error': 'Mistral API key is not configured in settings for image analysis. Please set MISTRAL_API_KEY.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                # Read image data
                image_data = uploaded_file.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                
                # Get Mistral client
                mistral_client = self._get_client()
                
                # Determine image format for data URL
                image_format = uploaded_file.content_type.split('/')[-1]
                image_data_url = f"data:{uploaded_file.content_type};base64,{image_base64}"
                
                prompt_text = """You are a health and nutrition advisor for Blood Hub Nepal. Analyze this blood report image and provide:

IMPORTANT RULES:
- NEVER recommend medicines, medications, drugs, or pharmaceutical products
- Only suggest natural foods and lifestyle changes
- Always advise consulting a doctor for medical treatment
- Focus on preventive health and nutrition through diet

ANALYSIS FORMAT:
1. **Health Issues Identified**: List any health concerns visible in the report
2. **Foods to Eat**: Recommend specific Nepalese foods with nutrients they provide:
   - Iron-rich: spinach, lentils, red meat, fortified grains, dates
   - Calcium-rich: milk, yogurt, sesame seeds, leafy greens
   - Protein: chickpeas, beans, fish, eggs, nuts
3. **Foods to Avoid**: List foods that may worsen the identified conditions
4. **Daily Lifestyle Tips**: Exercise and habit recommendations
5. **Additional Wellness Advice**: Other preventive health measures

Be specific, practical, and actionable."""
                
                # Prepare messages for Mistral multimodal
                messages = [
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt_text},
                        {"type": "image_url", "image_url": {"url": image_data_url}}
                    ]}
                ]
                
                # Analyze image using Mistral multimodal model
                response = mistral_client.chat.complete(
                    model="mistral-large-latest", # Using mistral-large-latest for multimodal capabilities
                    messages=messages
                )
                
                return Response({
                    'analysis': response.choices[0].message.content,
                    'status': 'success'
                })
            
        except ImportError as e:
            # This handles missing mistralai or google.generativeai itself
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            error_message = f"An unexpected error occurred while analyzing the file: {str(e)}"
            if "unauthorized" in str(e).lower() or "api key" in str(e).lower():
                error_message = "An API key issue occurred. Please check your Mistral API key configuration."
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
        blood_product_type = request.query_params.get('blood_product_type')
        sort_by = request.query_params.get('sort_by', 'hospital__name')  # Default sort by hospital name
        order = request.query_params.get('order', 'asc')  # Default order ascending

        queryset = BloodStock.objects.select_related('hospital')
        
        if blood_group:
            queryset = queryset.filter(blood_group=blood_group)
        if city:
            queryset = queryset.filter(hospital__city__icontains=city)
        if blood_product_type:
            queryset = queryset.filter(blood_product_type=blood_product_type)

        # Apply sorting
        if sort_by:
            if order == 'desc':
                sort_by = f'-{sort_by}'
            queryset = queryset.order_by(sort_by)

        serializer = BloodStockSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def analyze_report(self, request):
        """Analyze medical report and provide health/food recommendations"""
        try:
            report_text = request.data.get('report_text', '')
            report_type = request.data.get('report_type', 'general')
            
            if not report_text:
                return Response({'error': 'Report text is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not settings.MISTRAL_API_KEY:
                return Response({'error': 'Mistral API key is not configured in settings.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            client = self._get_client()
            
            prompt = f"""You are a health and nutrition advisor for Blood Hub Nepal. When analyzing medical reports, follow these rules:

RULES:
- NEVER recommend medicines, medications, drugs, or pharmaceutical products
- Only suggest natural foods and lifestyle changes
- Always advise consulting a doctor for medical treatment
- Focus on preventive health and nutrition
- Keep recommendations practical and actionable

Report Type: {report_type}
Report Content: {report_text}

Please provide:
1. Summary of key findings
2. Specific Nepalese foods to eat (iron-rich: spinach, lentils, red meat; calcium-rich: milk, yogurt, sesame; protein-rich: chickpeas, beans, fish)
3. Foods to avoid or limit
4. Daily lifestyle and exercise suggestions
5. Wellness tips"""
            
            response = client.chat.complete(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": prompt}]
            )
            
            return Response({'analysis': response.choices[0].message.content})
        except ImportError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            error_message = f"An error occurred while communicating with the AI service: {str(e)}"
            if "unauthorized" in str(e).lower() or "api key" in str(e).lower():
                error_message = "The provided Mistral API key is invalid or unauthorized. Please check your API key configuration and ensure it has the necessary permissions."
                return Response({'error': error_message}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BloodRequestViewSet(viewsets.ModelViewSet):
    """Manage blood requests and notify nearby donors via SMS."""

    queryset = BloodRequest.objects.all().select_related('created_by')
    serializer_class = BloodRequestSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        created_by = request.user if getattr(request, 'user', None) and request.user.is_authenticated else None
        blood_request = serializer.save(created_by=created_by)

        sms_summary = self._notify_matching_donors(blood_request)

        response_data = BloodRequestSerializer(blood_request, context=self.get_serializer_context()).data
        response_data['sms_summary'] = sms_summary

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def _notify_matching_donors(self, blood_request):
        donors = DonorProfile.objects.filter(
            blood_group=blood_request.blood_type,
            district__iexact=blood_request.district,
        ).exclude(phone__isnull=True).exclude(phone__exact='')

        summary = {
            'matched': donors.count(),
            'sent': 0,
            'failed': 0,
        }

        location_text = blood_request.location or f"{blood_request.city}, {blood_request.district}".strip(', ')
        message_text = (
            "URGENT BLOOD REQUEST\n\n"
            f"Blood Type: {blood_request.blood_type}\n"
            f"Location: {location_text}\n"
            f"Urgency: {blood_request.urgency}\n\n"
            "Your blood type matches! Please help save lives. Contact the hospital immediately.\n\n"
            "Reply STOP to unsubscribe."
        )

        for donor in donors:
            sent = send_blood_request_sms(
                donor.phone,
                blood_request.blood_type,
                location_text,
                blood_request.urgency,
            )

            SMSNotificationLog.objects.create(
                blood_request=blood_request,
                recipient=donor.user if donor.user_id else None,
                phone_number=donor.phone,
                message=message_text,
                status='sent' if sent else 'failed',
            )

            if sent:
                summary['sent'] += 1
            else:
                summary['failed'] += 1

        return summary

