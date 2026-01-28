"""
SMS API Views for sending SMS messages directly from backend
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.core.validators import validate_email
from .sms_service import (
    send_sms, send_bulk_sms, send_blood_request_sms, 
    TWILIO_ENABLED, SPARROW_ENABLED, SMS_PASAL_ENABLED, SMS_ENABLED, SMS_PROVIDER
)
import logging

logger = logging.getLogger(__name__)


class SMSViewSet(viewsets.ViewSet):
    """
    ViewSet for sending SMS messages
    """
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def send(self, request):
        """
        Send a single SMS message
        
        Request body:
        {
            "phone_number": "+1234567890",
            "message": "Your message here"
        }
        """
        phone_number = request.data.get('phone_number')
        message = request.data.get('message')

        if not phone_number:
            return Response(
                {'error': 'phone_number is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not message:
            return Response(
                {'error': 'message is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = send_sms(phone_number, message)

        if result['success']:
            return Response({
                'success': True,
                'message': 'SMS sent successfully',
                'message_sid': result['message_sid'],
                'phone_number': phone_number
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'error': result['error'],
                'phone_number': phone_number
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def send_bulk(self, request):
        """
        Send SMS to multiple phone numbers
        
        Request body:
        {
            "phone_numbers": ["+1234567890", "+9876543210"],
            "message": "Your message here"
        }
        """
        phone_numbers = request.data.get('phone_numbers', [])
        message = request.data.get('message')

        if not phone_numbers:
            return Response(
                {'error': 'phone_numbers array is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(phone_numbers, list):
            return Response(
                {'error': 'phone_numbers must be an array'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not message:
            return Response(
                {'error': 'message is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = send_bulk_sms(phone_numbers, message)

        return Response({
            'success': True,
            'message': 'Bulk SMS processing completed',
            'success_count': result['success_count'],
            'failed_count': result['failed_count'],
            'results': result['results']
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def status(self, request):
        """
        Check SMS service status
        """
        providers = []
        if SPARROW_ENABLED:
            providers.append('Sparrow SMS (Nepal)')
        if SMS_PASAL_ENABLED:
            providers.append('SMS Pasal (Nepal)')
        if TWILIO_ENABLED:
            providers.append('Twilio (International)')
        
        return Response({
            'enabled': SMS_ENABLED,
            'status': 'active' if SMS_ENABLED else 'disabled',
            'provider': SMS_PROVIDER,
            'providers_configured': providers,
            'sparrow_enabled': SPARROW_ENABLED,
            'sms_pasal_enabled': SMS_PASAL_ENABLED,
            'twilio_enabled': TWILIO_ENABLED,
            'message': f'SMS service is ready via {SMS_PROVIDER}' if SMS_ENABLED else 'SMS service is disabled. Configure Sparrow SMS, SMS Pasal, or Twilio.'
        })


class SMSAPIView(APIView):
    """
    Simple API view for sending SMS
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Send SMS endpoint
        
        POST /api/sms/send/
        {
            "phone_number": "+1234567890",
            "message": "Your message here"
        }
        """
        phone_number = request.data.get('phone_number')
        message = request.data.get('message')

        if not phone_number:
            return Response(
                {'error': 'phone_number is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not message:
            return Response(
                {'error': 'message is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = send_sms(phone_number, message)

        if result['success']:
            return Response({
                'success': True,
                'message': 'SMS sent successfully',
                'message_sid': result['message_sid']
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
