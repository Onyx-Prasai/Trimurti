from rest_framework import serializers
from .models import BloodPacket, TaRTimer, LocationUpdate, NotificationLog

class BloodPacketSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodPacket
        fields = ['id', 'blood_request', 'courier', 'pickup_time', 'status', 'initial_temperature']

class TaRTimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaRTimer
        fields = ['id', 'blood_packet', 'start_time', 'ambient_temperature', 'predicted_decay_time', 'critical_threshold_time']

class LocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationUpdate
        fields = ['id', 'courier', 'timestamp', 'latitude', 'longitude', 'traffic_jam_detected']

class NotificationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationLog
        fields = ['id', 'courier', 'message', 'timestamp']
