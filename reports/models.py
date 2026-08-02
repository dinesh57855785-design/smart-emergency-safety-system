from django.db import models
from django.conf import settings


class EmergencyReport(models.Model):
    sos_event = models.OneToOneField("sos.SOSEvent", on_delete=models.CASCADE, related_name="report")
    summary = models.TextField(blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.sos_event_id}"
