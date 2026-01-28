from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BloodPacket(models.Model):
    blood_request = models.ForeignKey('api.BloodRequest', on_delete=models.CASCADE)
    courier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='blood_packets')
    pickup_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='in_transit', choices=[('in_transit', 'In Transit'), ('delivered', 'Delivered')])
    initial_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Initial temperature in Celsius")

    def __str__(self):
        return f"Packet for request {self.blood_request.id} by courier {self.courier.username if self.courier else 'N/A'}"

class TaRTimer(models.Model):
    blood_packet = models.OneToOneField(BloodPacket, on_delete=models.CASCADE, related_name='tar_timer')
    start_time = models.DateTimeField(auto_now_add=True)
    ambient_temperature = models.DecimalField(max_digits=5, decimal_places=2, help_text="Ambient temperature at pickup in Celsius")
    predicted_decay_time = models.PositiveIntegerField(help_text="Predicted time in minutes for temperature to become critical")
    critical_threshold_time = models.PositiveIntegerField(help_text="Time in minutes when critical temperature is expected to be reached")

    def __str__(self):
        return f"Timer for {self.blood_packet.id}"

class LocationUpdate(models.Model):
    courier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='location_updates')
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    traffic_jam_detected = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Location for {self.courier.username} at {self.timestamp}"

class NotificationLog(models.Model):
    courier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_logs')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Notification for {self.courier.username} at {self.timestamp}"