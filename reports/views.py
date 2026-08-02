import csv
import io
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from . import services
from .models import ReportExport
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


@login_required
def dashboard(request):
    return render(request, 'reports/dashboard.html')


@login_required
def api_daily(request):
    data = services.daily_emergencies()
    # Normalize dates to strings
    out = [{'date': d['day'].isoformat() if d['day'] else None, 'count': d['count']} for d in data]
    return JsonResponse(out, safe=False)


@login_required
def api_weekly(request):
    data = services.weekly_emergencies()
    out = [{'week': d['week'].isoformat() if d['week'] else None, 'count': d['count']} for d in data]
    return JsonResponse(out, safe=False)


@login_required
def api_monthly(request):
    data = services.monthly_emergencies()
    out = [{'month': d['month'].isoformat() if d['month'] else None, 'count': d['count']} for d in data]
    return JsonResponse(out, safe=False)


@login_required
def api_user_activity(request):
    data = services.user_activity()
    return JsonResponse(data, safe=False)


@login_required
def api_emergency_types(request):
    data = services.emergency_type_stats()
    return JsonResponse(list(data), safe=False)


@login_required
def api_police_stats(request):
    data = services.police_notification_stats()
    return JsonResponse(list(data), safe=False)


@login_required
def api_sms_stats(request):
    data = services.sms_notification_stats()
    return JsonResponse(list(data), safe=False)


@login_required
def api_video_stats(request):
    data = services.video_session_stats()
    return JsonResponse(list(data), safe=False)


@login_required
def export_csv(request):
    report = request.GET.get('report')
    now = timezone.now()
    filename = f'report_{report}_{now.strftime("%Y%m%d%H%M%S")}.csv'
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    rows = []
    if report == 'daily':
        data = services.daily_emergencies()
        writer.writerow(['date', 'count'])
        for d in data:
            writer.writerow([d['day'].isoformat() if d['day'] else '', d['count']])
        rows = data
    elif report == 'weekly':
        data = services.weekly_emergencies()
        writer.writerow(['week', 'count'])
        for d in data:
            writer.writerow([d['week'].isoformat() if d['week'] else '', d['count']])
        rows = data
    elif report == 'monthly':
        data = services.monthly_emergencies()
        writer.writerow(['month', 'count'])
        for d in data:
            writer.writerow([d['month'].isoformat() if d['month'] else '', d['count']])
        rows = data
    elif report == 'user_activity':
        data = services.user_activity()
        writer.writerow(['user', 'count'])
        for d in data:
            writer.writerow([d['user'], d['count']])
        rows = data
    else:
        return JsonResponse({'status': 'error', 'error': 'unknown report'}, status=400)

    resp = HttpResponse(buffer.getvalue(), content_type='text/csv')
    resp['Content-Disposition'] = f'attachment; filename="{filename}"'

    # store export meta
    re = ReportExport.objects.create(user=request.user, report_type=report, file_type='csv', record_count=len(rows))
    return resp


@login_required
def export_pdf(request):
    report = request.GET.get('report')
    now = timezone.now()
    filename = f'report_{report}_{now.strftime("%Y%m%d%H%M%S")}.pdf'

    # Simple PDF using reportlab
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont('Helvetica-Bold', 16)
    p.drawString(72, 720, f'Report: {report}')
    p.setFont('Helvetica', 10)
    y = 700

    if report == 'daily':
        data = services.daily_emergencies()
        p.drawString(72, y, 'Date - Count')
        y -= 20
        for d in data:
            line = f"{d['day'].isoformat() if d['day'] else ''} - {d['count']}"
            p.drawString(72, y, line)
            y -= 14
            if y < 72:
                p.showPage(); y = 720
    elif report == 'user_activity':
        data = services.user_activity()
        p.drawString(72, y, 'User - Count')
        y -= 20
        for d in data:
            line = f"{d['user']} - {d['count']}"
            p.drawString(72, y, line)
            y -= 14
            if y < 72:
                p.showPage(); y = 720
    else:
        p.drawString(72, y, 'Report type not supported for PDF yet.')

    p.showPage()
    p.save()
    buffer.seek(0)
    re = ReportExport.objects.create(user=request.user, report_type=report, file_type='pdf', record_count=0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
