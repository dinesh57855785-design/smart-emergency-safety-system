from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from accounts.models import User
from contacts.models import TrustedContact
from profiles.models import Profile
from sos.models import SOSEvent
from notifications.models import NotificationLog


@login_required
def index(request):
    contacts = TrustedContact.objects.filter(user=request.user)
    events = SOSEvent.objects.filter(user=request.user)
    active_event = events.filter(status="active").first()
    profile, _ = Profile.objects.get_or_create(user=request.user)
    needs_review = profile.needs_review()
    return render(request, "dashboard/index.html", {
        "contacts": contacts,
        "events": events[:5],
        "active_event": active_event,
        "needs_review": needs_review,
        "contact_count": contacts.count(),
    })


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Admin access required.")
    users = User.objects.all().order_by("-date_joined")
    events = SOSEvent.objects.all().order_by("-triggered_at")[:50]
    active_events = SOSEvent.objects.filter(status="active")
    logs = NotificationLog.objects.all()[:50]
    return render(request, "dashboard/admin_dashboard.html", {
        "users": users,
        "events": events,
        "active_events": active_events,
        "logs": logs,
        "total_users": users.count(),
        "total_events": SOSEvent.objects.count(),
        "total_active": active_events.count(),
    })
