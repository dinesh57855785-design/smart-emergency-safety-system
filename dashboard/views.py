from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from notifications.models import SMSNotification
from police.models import PoliceNotification
from video.models import VideoSession
from reports.services import daily_emergencies, monthly_emergencies, emergency_type_stats
from sos.models import SosEvent
from contacts.models import EmergencyContact
from reports.models import ReportExport


@login_required
def index(request):
    # show recent SMS notifications related to user
    notifications = SMSNotification.objects.filter(sos_event__user=request.user)[:10]
    police_notifications = PoliceNotification.objects.filter(sos_event__user=request.user)[:10]
    video_sessions = VideoSession.objects.filter(sos_event__user=request.user, status='active')[:5]
    return render(request, 'dashboard/index.html', {'notifications': notifications, 'police_notifications': police_notifications, 'video_sessions': video_sessions})


@staff_member_required
def admin_dashboard(request):
    now = timezone.now()
    total_users = User.objects.count()
    total_contacts = EmergencyContact.objects.count()
    total_sos = SosEvent.objects.count()
    # define active as SOS in last 30 minutes
    active_sos = SosEvent.objects.filter(created_at__gt=now - timedelta(minutes=30)).count()
    completed_sos = total_sos - active_sos
    police_count = PoliceNotification.objects.count()
    sms_count = SMSNotification.objects.count()
    video_count = VideoSession.objects.count()
    reports_count = ReportExport.objects.count()
    recent_activities = SosEvent.objects.select_related('user').order_by('-created_at')[:10]

    context = {
        'total_users': total_users,
        'total_contacts': total_contacts,
        'total_sos': total_sos,
        'active_sos': active_sos,
        'completed_sos': completed_sos,
        'police_count': police_count,
        'sms_count': sms_count,
        'video_count': video_count,
        'reports_count': reports_count,
        'recent_activities': recent_activities,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@staff_member_required
def api_daily_sos(request):
    data = daily_emergencies()
    out = [{'date': d['day'].isoformat() if d['day'] else None, 'count': d['count']} for d in data]
    return JsonResponse(out, safe=False)


@staff_member_required
def api_monthly_sos(request):
    data = monthly_emergencies()
    out = [{'month': d['month'].isoformat() if d['month'] else None, 'count': d['count']} for d in data]
    return JsonResponse(out, safe=False)


@staff_member_required
def api_emergency_types(request):
    data = emergency_type_stats()
    return JsonResponse(list(data), safe=False)


@staff_member_required
def api_user_registrations(request):
    # return user registrations per day for last 30 days
    qs = User.objects.annotate(day=timezone.localtime('date_joined')).all()
    # simple implementation: return counts per day using ORM could be heavy; keep simple stub
    from django.db.models.functions import TruncDate
    qs = User.objects.annotate(day=TruncDate('date_joined')).values('day').annotate(count=__import__('django.db.models').db.models.Count('id')).order_by('day')
    out = [{'date': d['day'].isoformat() if d['day'] else None, 'count': d['count']} for d in qs]
    return JsonResponse(out, safe=False)
