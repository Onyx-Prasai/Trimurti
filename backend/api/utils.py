"""
BloodSync Nepal - Utility Functions
Alert system, notifications, and helper functions
"""

from django.utils import timezone
from django.db.models import Sum, Q
from math import radians, cos, sin, asin, sqrt
from .models import BloodStock, StockAlert, Hospital, DonationDrive, BLOOD_GROUP_CHOICES, DonorProfile


def check_and_create_alerts():
    """
    Check all blood stocks and create alerts for low/critical levels.
    Returns the number of new alerts created.
    
    Thresholds:
    - Emergency: < 3 units
    - Critical: < 5 units
    - Low: < 15 units
    """
    alerts_created = 0
    
    for stock in BloodStock.objects.select_related('hospital'):
        alert_level = None
        threshold = 0
        
        if stock.units_available < 3:
            alert_level = 'emergency'
            threshold = 3
        elif stock.units_available < 5:
            alert_level = 'critical'
            threshold = 5
        elif stock.units_available < 15:
            alert_level = 'low'
            threshold = 15
        
        if alert_level:
            # Check if there's already an active alert for this combination
            existing_alert = StockAlert.objects.filter(
                hospital=stock.hospital,
                blood_group=stock.blood_group,
                resolved_at__isnull=True
            ).first()
            
            if not existing_alert:
                # Create new alert
                StockAlert.objects.create(
                    hospital=stock.hospital,
                    blood_group=stock.blood_group,
                    alert_level=alert_level,
                    threshold=threshold,
                    current_units=stock.units_available
                )
                alerts_created += 1
        else:
            # Stock is sufficient, resolve any existing alerts
            StockAlert.objects.filter(
                hospital=stock.hospital,
                blood_group=stock.blood_group,
                resolved_at__isnull=True
            ).update(resolved_at=timezone.now())
    
    return alerts_created


def suggest_donation_drives():
    """
    Analyze regional shortages and suggest donation drives.
    Returns list of suggested drives.
    """
    suggestions = []
    
    # Group by city and blood group
    cities = Hospital.objects.filter(is_active=True).values_list('city', flat=True).distinct()
    
    for city in cities:
        city_stocks = BloodStock.objects.filter(hospital__city=city, hospital__is_active=True)
        
        for blood_group_code, blood_group_name in BLOOD_GROUP_CHOICES:
            total_units = city_stocks.filter(blood_group=blood_group_code).aggregate(
                total=Sum('units_available')
            )['total'] or 0
            
            hospitals_count = city_stocks.filter(blood_group=blood_group_code).count()
            
            if hospitals_count == 0:
                continue
            
            avg_units_per_hospital = total_units / hospitals_count if hospitals_count > 0 else 0
            
            # Determine urgency
            urgency = None
            target_units = 0
            
            if avg_units_per_hospital < 5:
                urgency = 'critical'
                target_units = 200
            elif avg_units_per_hospital < 10:
                urgency = 'urgent'
                target_units = 150
            elif avg_units_per_hospital < 20:
                urgency = 'normal'
                target_units = 100
            
            if urgency:
                suggestions.append({
                    'city': city,
                    'blood_groups': [blood_group_code],
                    'urgency': urgency,
                    'target_units': target_units,
                    'current_avg': round(avg_units_per_hospital, 1),
                    'hospitals_affected': hospitals_count
                })
    
    return suggestions


def auto_create_donation_drives():
    """
    Automatically create donation drives based on critical shortages.
    Returns number of drives created.
    """
    from datetime import timedelta
    
    suggestions = suggest_donation_drives()
    drives_created = 0
    
    for suggestion in suggestions:
        if suggestion['urgency'] in ['critical', 'urgent']:
            # Check if there's already an active drive for this city/blood group
            existing_drive = DonationDrive.objects.filter(
                city=suggestion['city'],
                blood_groups__contains=suggestion['blood_groups'],
                status__in=['planned', 'active']
            ).first()
            
            if not existing_drive:
                start_date = timezone.now().date()
                end_date = start_date + timedelta(days=14)  # 2-week campaign
                
                DonationDrive.objects.create(
                    title=f"Emergency Blood Drive - {suggestion['city']}",
                    city=suggestion['city'],
                    blood_groups=suggestion['blood_groups'],
                    urgency=suggestion['urgency'],
                    target_units=suggestion['target_units'],
                    start_date=start_date,
                    end_date=end_date,
                    status='active',
                    description=f"Critical shortage detected for {', '.join(suggestion['blood_groups'])} "
                                f"in {suggestion['city']}. Current average: {suggestion['current_avg']} units "
                                f"per hospital. Target: {suggestion['target_units']} units."
                )
                drives_created += 1
    
    return drives_created


def get_hospital_stock_summary(hospital):
    """
    Get a summary of blood stock for a hospital.
    
    Args:
        hospital: Hospital instance
    
    Returns:
        dict with stock information
    """
    stock_data = {}
    total_units = 0
    low_stock_groups = []
    
    for blood_group_code, blood_group_name in BLOOD_GROUP_CHOICES:
        stock = hospital.stock.filter(blood_group=blood_group_code).first()
        units = stock.units_available if stock else 0
        
        stock_data[blood_group_code] = {
            'units': units,
            'status': get_stock_status(units),
            'updated_at': stock.updated_at.isoformat() if stock else None
        }
        
        total_units += units
        
        if units < 15:
            low_stock_groups.append(blood_group_code)
    
    return {
        'stock_by_group': stock_data,
        'total_units': total_units,
        'low_stock_groups': low_stock_groups,
        'hospital': {
            'code': hospital.code,
            'name': hospital.name,
            'city': hospital.city
        }
    }


def get_stock_status(units):
    """
    Get human-readable status for stock units.
    
    Args:
        units: int, number of units
    
    Returns:
        str: status label
    """
    if units < 3:
        return 'EMERGENCY'
    elif units < 5:
        return 'CRITICAL'
    elif units < 15:
        return 'LOW'
    elif units < 30:
        return 'MODERATE'
    else:
        return 'GOOD'


def calculate_national_statistics():
    """
    Calculate national-level blood stock statistics.
    
    Returns:
        dict with comprehensive statistics
    """
    total_hospitals = Hospital.objects.filter(is_active=True).count()
    
    # Total units by blood group
    blood_group_totals = {}
    for bg_code, bg_name in BLOOD_GROUP_CHOICES:
        total = BloodStock.objects.filter(blood_group=bg_code).aggregate(
            total=Sum('units_available')
        )['total'] or 0
        blood_group_totals[bg_code] = total
    
    # Overall total
    total_units = sum(blood_group_totals.values())
    
    # Critical hospitals (any blood group < 5)
    critical_hospitals = set()
    for stock in BloodStock.objects.filter(units_available__lt=5):
        critical_hospitals.add(stock.hospital.id)
    
    # Active alerts
    active_alerts = StockAlert.objects.filter(resolved_at__isnull=True).count()
    
    # City-wise breakdown
    cities = Hospital.objects.filter(is_active=True).values_list('city', flat=True).distinct()
    city_stats = {}
    
    for city in cities:
        city_total = BloodStock.objects.filter(
            hospital__city=city,
            hospital__is_active=True
        ).aggregate(total=Sum('units_available'))['total'] or 0
        
        city_hospitals = Hospital.objects.filter(city=city, is_active=True).count()
        
        city_stats[city] = {
            'total_units': city_total,
            'hospitals_count': city_hospitals,
            'avg_units_per_hospital': round(city_total / city_hospitals, 1) if city_hospitals > 0 else 0
        }
    
    return {
        'total_hospitals': total_hospitals,
        'total_units': total_units,
        'blood_group_distribution': blood_group_totals,
        'critical_hospitals_count': len(critical_hospitals),
        'active_alerts': active_alerts,
        'city_statistics': city_stats,
        'timestamp': timezone.now().isoformat()
    }


def send_low_stock_notification(alert):
    """
    Send notification for low stock alert.
    This is a placeholder - integrate with email/SMS service.
    
    Args:
        alert: StockAlert instance
    """
    # TODO: Integrate with email service (SendGrid, AWS SES, etc.)
    # TODO: Integrate with SMS service (Twilio, etc.)
    
    message = f"""
    BLOODSYNC NEPAL - {alert.alert_level.upper()} ALERT
    
    Hospital: {alert.hospital.name}
    City: {alert.hospital.city}
    Blood Group: {alert.blood_group}
    Current Stock: {alert.current_units} units
    Threshold: {alert.threshold} units
    
    Action Required: Please arrange blood collection drives or transfer from nearby facilities.
    """
    
    # For now, just log it
    print(f"[ALERT] {alert.hospital.code} - {alert.blood_group}: {alert.alert_level}")
    print(message)
    
    # Mark as notified
    alert.notified = True
    alert.save()
    
    return True


def get_nearby_hospitals_with_stock(hospital, blood_group, radius_km=50):
    """
    Find nearby hospitals with available stock of a specific blood group.
    This is a simplified version - in production, use PostGIS for accurate distance calculation.
    
    Args:
        hospital: Hospital instance
        blood_group: str, blood group code
        radius_km: int, search radius in kilometers
    
    Returns:
        list of hospitals with stock information
    """
    # Simple implementation - filter by same city
    # In production, calculate actual distance using lat/long
    nearby = Hospital.objects.filter(
        is_active=True,
        city=hospital.city
    ).exclude(id=hospital.id)
    
    results = []
    for h in nearby:
        stock = h.stock.filter(blood_group=blood_group, units_available__gt=5).first()
        if stock:
            results.append({
                'hospital': {
                    'code': h.code,
                    'name': h.name,
                    'city': h.city,
                    'address': h.address
                },
                'units_available': stock.units_available,
                'updated_at': stock.updated_at.isoformat()
            })
    
    return results


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points on Earth (in meters)
    using the Haversine formula.
    
    Args:
        lat1, lon1: Latitude and longitude of first point (in decimal degrees)
        lat2, lon2: Latitude and longitude of second point (in decimal degrees)
    
    Returns:
        float: Distance in meters
    """
    if not all([lat1, lon1, lat2, lon2]):
        return None
    
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in meters
    r = 6371000
    
    return c * r


def find_donors_within_radius(request_lat, request_lon, blood_type, radius_meters=500, max_radius_meters=10000):
    """
    Find donors within a specified radius from the request location.
    Expands radius if not enough donors found.
    
    Args:
        request_lat: Latitude of blood request location
        request_lon: Longitude of blood request location
        blood_type: Blood type needed
        radius_meters: Starting radius in meters (default: 500m)
        max_radius_meters: Maximum radius to search (default: 10km)
    
    Returns:
        dict: {
            'donors': list of DonorProfile objects,
            'radius_used': final radius used in meters,
            'total_found': number of donors found
        }
    """
    if not request_lat or not request_lon:
        return {'donors': [], 'radius_used': 0, 'total_found': 0}
    
    current_radius = radius_meters
    donors_found = []
    
    # Get all donors with matching blood type and location data
    all_donors = DonorProfile.objects.filter(
        blood_group=blood_type,
        latitude__isnull=False,
        longitude__isnull=False,
        location_consent=True,
        phone__isnull=False
    ).exclude(phone__exact='')
    
    # Expand radius until we find donors or reach max radius
    while current_radius <= max_radius_meters:
        for donor in all_donors:
            distance = calculate_distance(
                request_lat, request_lon,
                float(donor.latitude), float(donor.longitude)
            )
            
            if distance and distance <= current_radius:
                # Check if donor is not already in the list
                if donor.id not in [d.id for d in donors_found]:
                    donors_found.append(donor)
        
        # If we found donors, return them
        if donors_found:
            return {
                'donors': donors_found,
                'radius_used': current_radius,
                'total_found': len(donors_found)
            }
        
        # Expand radius: 500m -> 1km -> 2km -> 5km -> 10km
        if current_radius < 1000:
            current_radius = 1000
        elif current_radius < 2000:
            current_radius = 2000
        elif current_radius < 5000:
            current_radius = 5000
        else:
            current_radius = max_radius_meters
    
    return {
        'donors': donors_found,
        'radius_used': current_radius,
        'total_found': len(donors_found)
    }
