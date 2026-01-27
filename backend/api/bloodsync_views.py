"""
BloodSync Nepal - Additional API Views
Real-time blood inventory management endpoints
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from django.db.models import Sum, Count, Q, Max
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict

from .models import (
    Hospital, BloodStock, Transaction, StockAlert, DonationDrive, BLOOD_GROUP_CHOICES
)
from .serializers import (
    HospitalSerializer, BloodStockSerializer, TransactionSerializer,
    StockAlertSerializer, DonationDriveSerializer
)


class PublicBloodStockView(APIView):
    """
    Public endpoint for searching blood availability across hospitals.
    GET /api/v1/public/blood-stock
    Query params: city, blood_group, min_units
    """
    permission_classes = [AllowAny]

    def get(self, request):
        city = request.query_params.get('city')
        blood_group = request.query_params.get('blood_group')
        min_units = request.query_params.get('min_units', 0)

        try:
            min_units = int(min_units)
        except ValueError:
            min_units = 0

        # Query active hospitals
        hospitals = Hospital.objects.filter(is_active=True)
        if city:
            hospitals = hospitals.filter(city__icontains=city)

        results = []
        for hospital in hospitals:
            stock_queryset = hospital.stock.all()
            if blood_group:
                stock_queryset = stock_queryset.filter(blood_group=blood_group)
            if min_units > 0:
                stock_queryset = stock_queryset.filter(units_available__gte=min_units)

            # Build stock dictionary
            stock_dict = {}
            latest_update = None
            for stock in stock_queryset:
                stock_dict[stock.blood_group] = {
                    'units': stock.units_available,
                    'updated_at': stock.updated_at.isoformat()
                }
                if not latest_update or stock.updated_at > latest_update:
                    latest_update = stock.updated_at

            if stock_dict:  # Only include hospitals with matching stock
                results.append({
                    'hospital': HospitalSerializer(hospital).data,
                    'stock': stock_dict,
                    'last_updated': latest_update.isoformat() if latest_update else None
                })

        return Response({
            'results': results,
            'total_hospitals': len(results),
            'query': {
                'city': city,
                'blood_group': blood_group,
                'min_units': min_units
            },
            'timestamp': timezone.now().isoformat()
        })


class BloodAvailabilityByCityView(APIView):
    """
    Aggregated blood availability by city.
    GET /api/v1/public/blood-availability/{city}
    """
    permission_classes = [AllowAny]

    def get(self, request, city):
        hospitals = Hospital.objects.filter(is_active=True, city__icontains=city)
        
        if not hospitals.exists():
            return Response({
                'error': f'No hospitals found in {city}',
                'city': city,
                'total_hospitals': 0
            }, status=status.HTTP_404_NOT_FOUND)

        # Aggregate stock across all hospitals in city
        aggregated = defaultdict(int)
        latest_updates = {}
        
        for hospital in hospitals:
            for stock in hospital.stock.all():
                aggregated[stock.blood_group] += stock.units_available
                if stock.blood_group not in latest_updates or stock.updated_at > latest_updates[stock.blood_group]:
                    latest_updates[stock.blood_group] = stock.updated_at

        return Response({
            'city': city,
            'total_hospitals': hospitals.count(),
            'aggregated_stock': dict(aggregated),
            'last_updated_by_group': {k: v.isoformat() for k, v in latest_updates.items()},
            'timestamp': timezone.now().isoformat()
        })


class AdminAnalyticsView(APIView):
    """
    National blood stock analytics for admin/health authorities.
    GET /api/v1/admin/analytics/national
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Total units across all hospitals
        total_units = BloodStock.objects.aggregate(total=Sum('units_available'))['total'] or 0

        # Critical shortages (< 5 units)
        critical_stocks = BloodStock.objects.filter(units_available__lt=5).select_related('hospital')
        critical_shortages = []
        for stock in critical_stocks:
            critical_shortages.append({
                'hospital': stock.hospital.name,
                'city': stock.hospital.city,
                'blood_group': stock.blood_group,
                'units_available': stock.units_available
            })

        # Low stock count
        low_stock_count = BloodStock.objects.filter(units_available__lt=15).count()

        # Active alerts
        active_alerts = StockAlert.objects.filter(resolved_at__isnull=True).count()

        # Trend analysis (last 7 days vs previous 7 days)
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        two_weeks_ago = now - timedelta(days=14)

        recent_donations = Transaction.objects.filter(
            timestamp__gte=week_ago,
            units_change__gt=0
        ).aggregate(total=Sum('units_change'))['total'] or 0

        previous_donations = Transaction.objects.filter(
            timestamp__gte=two_weeks_ago,
            timestamp__lt=week_ago,
            units_change__gt=0
        ).aggregate(total=Sum('units_change'))['total'] or 0

        trend = 'stable'
        if recent_donations > previous_donations * 1.1:
            trend = 'increasing'
        elif recent_donations < previous_donations * 0.9:
            trend = 'declining'

        # Blood group distribution
        blood_group_distribution = {}
        for bg_code, bg_name in BLOOD_GROUP_CHOICES:
            total = BloodStock.objects.filter(blood_group=bg_code).aggregate(
                total=Sum('units_available')
            )['total'] or 0
            blood_group_distribution[bg_code] = total

        return Response({
            'total_units': total_units,
            'critical_shortages': critical_shortages,
            'low_stock_alerts': low_stock_count,
            'active_alerts': active_alerts,
            'trend': trend,
            'blood_group_distribution': blood_group_distribution,
            'statistics': {
                'total_hospitals': Hospital.objects.filter(is_active=True).count(),
                'total_transactions_last_7_days': Transaction.objects.filter(
                    timestamp__gte=week_ago
                ).count(),
                'recent_donations': recent_donations,
                'previous_donations': previous_donations
            },
            'timestamp': timezone.now().isoformat()
        })


class StockAlertViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View and manage stock alerts.
    GET /api/v1/admin/alerts
    """
    queryset = StockAlert.objects.all()
    serializer_class = StockAlertSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = StockAlert.objects.select_related('hospital')
        
        # Filter by resolution status
        resolved = self.request.query_params.get('resolved')
        if resolved == 'false':
            queryset = queryset.filter(resolved_at__isnull=True)
        elif resolved == 'true':
            queryset = queryset.filter(resolved_at__isnull=False)

        # Filter by alert level
        alert_level = self.request.query_params.get('alert_level')
        if alert_level:
            queryset = queryset.filter(alert_level=alert_level)

        return queryset.order_by('-triggered_at')


class DonationDriveViewSet(viewsets.ModelViewSet):
    """
    Manage donation drive campaigns.
    """
    queryset = DonationDrive.objects.all()
    serializer_class = DonationDriveSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = DonationDrive.objects.all()
        
        # Filter by status
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # Filter by city
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        # Only active drives
        active_only = self.request.query_params.get('active_only')
        if active_only == 'true':
            today = timezone.now().date()
            queryset = queryset.filter(
                start_date__lte=today,
                end_date__gte=today,
                status='active'
            )
        
        return queryset.order_by('-start_date')

    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """Update collected units for a donation drive."""
        drive = self.get_object()
        collected = request.data.get('collected_units')
        
        if collected is None:
            return Response({'error': 'collected_units is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            collected = int(collected)
            if collected < 0:
                raise ValueError("Collected units cannot be negative")
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        drive.collected_units += collected
        
        # Auto-complete if target reached
        if drive.collected_units >= drive.target_units and drive.status == 'active':
            drive.status = 'completed'
        
        drive.save()
        return Response(DonationDriveSerializer(drive).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def hospital_list_public(request):
    """
    Simple list of all active hospitals with their locations.
    GET /api/v1/public/hospitals
    """
    hospitals = Hospital.objects.filter(is_active=True).values(
        'code', 'name', 'city', 'address', 'latitude', 'longitude'
    )
    
    return Response({
        'hospitals': list(hospitals),
        'count': len(hospitals),
        'timestamp': timezone.now().isoformat()
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def check_stock_alerts(request):
    """
    Utility endpoint to manually trigger stock alert check.
    POST /api/v1/admin/check-alerts
    
    This would normally run as a scheduled task (Celery).
    """
    from .utils import check_and_create_alerts
    
    alerts_created = check_and_create_alerts()
    
    return Response({
        'message': f'Stock alert check completed',
        'alerts_created': alerts_created,
        'timestamp': timezone.now().isoformat()
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def blood_stock_map_data(request):
    """
    Get all hospital locations with current stock for map visualization.
    GET /api/v1/public/map-data
    """
    hospitals = Hospital.objects.filter(is_active=True).prefetch_related('stock')
    
    map_data = []
    for hospital in hospitals:
        if hospital.latitude and hospital.longitude:
            stock_summary = {}
            total_units = 0
            for stock in hospital.stock.all():
                stock_summary[stock.blood_group] = stock.units_available
                total_units += stock.units_available
            
            map_data.append({
                'id': str(hospital.id),
                'code': hospital.code,
                'name': hospital.name,
                'city': hospital.city,
                'address': hospital.address,
                'position': {
                    'lat': float(hospital.latitude),
                    'lng': float(hospital.longitude)
                },
                'stock': stock_summary,
                'total_units': total_units
            })
    
    return Response({
        'hospitals': map_data,
        'count': len(map_data),
        'timestamp': timezone.now().isoformat()
    })
