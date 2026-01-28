from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta

from .models import BloodPacket, TaRTimer, LocationUpdate, NotificationLog, User
from api.models import BloodRequest
from .serializers import BloodPacketSerializer, TaRTimerSerializer, LocationUpdateSerializer, NotificationLogSerializer
from .thermal_decay import calculate_tar
from .weather_api import get_ambient_temperature

class TimerViewSet(viewsets.ViewSet):
    """
    ViewSet for managing the Time-at-Risk (TaR) Timer for blood packets.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='pickup')
    def pickup_packet(self, request):
        """
        Action to be called when a courier picks up a blood packet.
        This starts the TaR timer.
        """
        blood_request_id = request.data.get('blood_request_id')
        initial_temperature = request.data.get('initial_temperature', 4.0) # Assume 4C if not provided

        if not blood_request_id:
            return Response({"error": "blood_request_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            blood_request = BloodRequest.objects.get(id=blood_request_id)
        except BloodRequest.DoesNotExist:
            return Response({"error": "BloodRequest not found"}, status=status.HTTP_404_NOT_FOUND)

        courier = request.user
        
        # For now, we'll use a fixed location for Kathmandu for the weather API
        kathmandu_lat = 27.7172
        kathmandu_lon = 85.3240
        
        ambient_temp = get_ambient_temperature(kathmandu_lat, kathmandu_lon)
        
        predicted_decay_time = calculate_tar(initial_temperature, ambient_temp)
        critical_threshold_time = predicted_decay_time * 0.8 # 80% of the decay time

        # Create the BloodPacket and TaRTimer
        blood_packet = BloodPacket.objects.create(
            blood_request=blood_request,
            courier=courier,
            initial_temperature=initial_temperature
        )
        
        tar_timer = TaRTimer.objects.create(
            blood_packet=blood_packet,
            ambient_temperature=ambient_temp,
            predicted_decay_time=predicted_decay_time,
            critical_threshold_time=critical_threshold_time
        )
        
        return Response({
            "message": "TaR Timer started.",
            "blood_packet": BloodPacketSerializer(blood_packet).data,
            "tar_timer": TaRTimerSerializer(tar_timer).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='update-location')
    def update_location(self, request):
        """
        Action for the courier's app to periodically update its location.
        This will check for traffic jams and send notifications if needed.
        """
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        traffic_jam_detected = request.data.get('traffic_jam_detected', False)

        if not latitude or not longitude:
            return Response({"error": "latitude and longitude are required"}, status=status.HTTP_400_BAD_REQUEST)

        courier = request.user
        
        LocationUpdate.objects.create(
            courier=courier,
            latitude=latitude,
            longitude=longitude,
            traffic_jam_detected=traffic_jam_detected
        )
        
        # Check all active blood packets for this courier
        active_packets = BloodPacket.objects.filter(courier=courier, status='in_transit')
        
        notifications = []
        for packet in active_packets:
            timer = packet.tar_timer
            
            time_since_pickup = (timezone.now() - packet.pickup_time).total_seconds() / 60 # in minutes
            
            # If a traffic jam is detected, recalculate the TaR with a higher ambient temp
            if traffic_jam_detected:
                # Simulate a higher ambient temperature due to traffic
                new_ambient_temp = timer.ambient_temperature + 5 
                predicted_decay_time = calculate_tar(packet.initial_temperature, new_ambient_temp)
                critical_threshold_time = predicted_decay_time * 0.8
                
                # Update the timer
                timer.predicted_decay_time = predicted_decay_time
                timer.critical_threshold_time = critical_threshold_time
                timer.save()

            if time_since_pickup >= timer.critical_threshold_time:
                # For now, we just log the notification.
                # A full implementation would send a push notification.
                message = "Critical Temperature Warning: Stop at the nearest pharmacy to replace ice packs immediately."
                
                # Avoid sending multiple notifications for the same packet
                if not NotificationLog.objects.filter(courier=courier, message=message, timestamp__gte=timezone.now() - timedelta(minutes=5)).exists():
                    notification = NotificationLog.objects.create(
                        courier=courier,
                        message=message
                    )
                    notifications.append(NotificationLogSerializer(notification).data)

        if notifications:
            return Response({
                "message": "Location updated. Critical notifications sent.",
                "notifications": notifications
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Location updated successfully."}, status=status.HTTP_200_OK)