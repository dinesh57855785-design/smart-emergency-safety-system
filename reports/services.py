from django.db.models import Count
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from sos.models import SosEvent
from notifications.models import SMSNotification
from police.models import PoliceNotification
from video.models import VideoSession
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


def daily_emergencies(days=30):
    qs = SosEvent.objects.annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).order_by('day')
    return list(qs)


def weekly_emergencies(weeks=12):
    qs = SosEvent.objects.annotate(week=TruncWeek('created_at')).values('week').annotate(count=Count('id')).order_by('week')
    return list(qs)


def monthly_emergencies(months=12):
    qs = SosEvent.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    return list(qs)


def user_activity(top_n=20):
    qs = User.objects.annotate(emergencies=Count('sosevent')).order_by('-emergencies')[:top_n]
    return [{'user': u.username, 'count': u.emergencies} for u in qs]


def emergency_type_stats():
    # assuming SosEvent has a 'message' or 'type' — we will group by message placeholder
    qs = SosEvent.objects.values('message').annotate(count=Count('id')).order_by('-count')
    return list(qs)


def police_notification_stats():
    qs = PoliceNotification.objects.values('status').annotate(count=Count('id'))
    return list(qs)


def sms_notification_stats():
    qs = SMSNotification.objects.values('status').annotate(count=Count('id'))
    return list(qs)


def video_session_stats():
    qs = VideoSession.objects.values('status').annotate(count=Count('id'))
    return list(qs)


def recent_emergencies(limit=50):
    return list(SosEvent.objects.select_related('user').order_by('-created_at')[:limit])
