import csv
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from sos.models import SOSEvent


@login_required
def reports_dashboard(request):
    events = SOSEvent.objects.filter(user=request.user).select_related("user")
    total = events.count()
    active = events.filter(status="active").count()
    resolved = events.filter(status="resolved").count()
    return render(request, "reports/dashboard.html", {
        "events": events,
        "total": total,
        "active": active,
        "resolved": resolved,
    })


@login_required
def export_report(request):
    events = SOSEvent.objects.filter(user=request.user)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="emergency_report.csv"'
    writer = csv.writer(response)
    writer.writerow([
        "SOS ID", "User", "Date", "Time", "Location", "Contacts Notified",
        "Police Station", "SMS Status", "Video Status", "Voice Status", "Status",
    ])
    for e in events:
        writer.writerow([
            str(e.id), e.user.email, e.triggered_at.date(), e.triggered_at.time(),
            e.location_url, e.notified_contacts.count(),
            e.police_station_name, e.sms_status, e.video_status, e.voice_status, e.status,
        ])
    return response
