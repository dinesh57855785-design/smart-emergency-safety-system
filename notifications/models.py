from django.db import models
from django.utils import timezone


class SMSNotification(models.Model):
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]

    sos_event = models.ForeignKey('sos.SosEvent', on_delete=models.CASCADE, related_name='sms_notifications')
    contact = models.ForeignKey('contacts.EmergencyContact', on_delete=models.SET_NULL, null=True, blank=True)
    to_number = models.CharField(max_length=50)
    message = models.TextField()
    twilio_sid = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')
    response = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'SMS to {self.to_number} ({self.status})'
