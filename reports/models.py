from django.db import models
from django.contrib.auth.models import User


class ReportExport(models.Model):
    FILE_TYPES = [
        ('csv', 'CSV'),
        ('pdf', 'PDF'),
    ]
    REPORT_TYPES = [
        ('daily', 'Daily Emergencies'),
        ('weekly', 'Weekly Emergencies'),
        ('monthly', 'Monthly Emergencies'),
        ('user_activity', 'User Activity'),
        ('emergency_types', 'Emergency Type Stats'),
        ('police_stats', 'Police Notification Stats'),
        ('sms_stats', 'SMS Notification Stats'),
        ('video_stats', 'Video Session Stats'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    record_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.get_report_type_display()} ({self.file_type}) by {self.user} at {self.created_at}"
