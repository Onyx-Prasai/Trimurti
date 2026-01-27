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
import math

from .models import (
    Hospital, BloodStock, Transaction, StockAlert, DonationDrive, BLOOD_GROUP_CHOICES, DonorProfile
)
from .serializers import (
    HospitalSerializer, BloodStockSerializer, TransactionSerializer,
    StockAlertSerializer, DonationDriveSerializer, NearbyDonorRequestSerializer
)

PRIORITY_CITIES = ['Kathmandu', 'Bhaktapur', 'Lalitpur', 'Pokhara']


def haversine_km(lat1, lon1, lat2, lon2):
    """Return distance in kilometers between two lat/long points."""
    r = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


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


class NearbyDonorLocatorView(APIView):
    """Locate consented donors near a hospital with critical vs normal radius rules."""

    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = NearbyDonorRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        hospital_qs = Hospital.objects.filter(is_active=True)
        if data.get('hospital_id'):
            hospital_qs = hospital_qs.filter(id=data['hospital_id'])
        if data.get('hospital_code'):
            hospital_qs = hospital_qs.filter(code=data['hospital_code'])
        hospital = hospital_qs.first()

        if not hospital:
            return Response({'error': 'Hospital not found or inactive'}, status=status.HTTP_404_NOT_FOUND)

        if hospital.latitude is None or hospital.longitude is None:
            return Response({'error': 'Hospital is missing location coordinates'}, status=status.HTTP_400_BAD_REQUEST)

        start_radius = 0.5 if data['is_critical'] else 2.0
        max_radius = data['max_radius_km']
        step = data['radius_step_km']
        min_needed = data['min_donor_count']

        donor_qs = DonorProfile.objects.filter(
            blood_group=data['blood_group'],
            location_consent=True,
            latitude__isnull=False,
            longitude__isnull=False,
        ).select_related('user')

        limit_cities = data.get('limit_cities') or []
        if limit_cities:
            city_query = Q()
            for city in limit_cities:
                city_query |= Q(district__iexact=city)
            donor_qs = donor_qs.filter(city_query)

        hospital_lat = float(hospital.latitude)
        hospital_lng = float(hospital.longitude)

        candidates = []
        for donor in donor_qs:
            try:
                donor_lat = float(donor.latitude)
                donor_lng = float(donor.longitude)
            except (TypeError, ValueError):
                continue

            if not donor.can_donate():
                continue

            distance = haversine_km(hospital_lat, hospital_lng, donor_lat, donor_lng)
            candidates.append((distance, donor))

        candidates.sort(key=lambda item: item[0])

        radius = start_radius
        selected = []
        while radius <= max_radius:
            selected = [
                {
                    'donor_id': donor.id,
                    'username': donor.user.username,
                    'district': donor.district,
                    'blood_group': donor.blood_group,
                    'distance_km': round(distance, 3),
                    'phone': donor.phone,
                    'last_donation_date': donor.last_donation_date,
                }
                for distance, donor in candidates
                if distance <= radius
            ]

            if len(selected) >= min_needed or radius >= max_radius:
                break

            radius += step

        radius_used = min(radius, max_radius)

        return Response({
            'hospital': HospitalSerializer(hospital).data,
            'search': {
                'start_radius_km': start_radius,
                'max_radius_km': max_radius,
                'step_km': step,
                'radius_used_km': radius_used,
                'is_critical': data['is_critical'],
                'blood_group': data['blood_group'],
                'blood_product': data['blood_product'],
                'min_donor_count': min_needed,
                'candidates_evaluated': len(candidates),
                'limit_cities': limit_cities,
            },
            'donors_found': selected,
            'count': len(selected),
            'timestamp': timezone.now().isoformat(),
        })


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

    cities_param = request.query_params.get('cities')
    if cities_param:
        city_list = [city.strip() for city in cities_param.split(',') if city.strip()]
        if city_list:
            city_query = Q()
            for city in city_list:
                city_query |= Q(city__iexact=city)
            hospitals = hospitals.filter(city_query)
    
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


@api_view(['GET'])
@permission_classes([AllowAny])
def priority_hospitals(request):
    """Return map-ready hospitals restricted to the four priority cities."""
    city_query = Q()
    for city in PRIORITY_CITIES:
        city_query |= Q(city__iexact=city)

    hospitals = Hospital.objects.filter(is_active=True).filter(city_query).prefetch_related('stock')

    hospitals = hospitals.filter(latitude__isnull=False, longitude__isnull=False)

    response_data = []
    for hospital in hospitals:
        stock_summary = {stock.blood_group: stock.units_available for stock in hospital.stock.all()}
        response_data.append({
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
            'total_units': sum(stock_summary.values()),
        })

    return Response({
        'hospitals': response_data,
        'count': len(response_data),
        'cities': PRIORITY_CITIES,
        'timestamp': timezone.now().isoformat()
    })
