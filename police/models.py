from django.db import models


class PoliceStation(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    place_id = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=80, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PoliceNotification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('acknowledged', 'Acknowledged'),
        ('failed', 'Failed'),
    ]

    sos_event = models.ForeignKey('sos.SosEvent', on_delete=models.CASCADE, related_name='police_notifications')
    police_station = models.ForeignKey(PoliceStation, on_delete=models.SET_NULL, null=True, blank=True)
    payload = models.TextField(help_text='JSON payload sent to police or notes', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    response = models.TextField(blank=True, null=True)
    notified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-notified_at']

    def __str__(self):
        station = self.police_station.name if self.police_station else 'Unknown'
        return f'PoliceNotification to {station} ({self.status})'
