from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import NotificationLog


@login_required
def notification_list(request):
    logs = NotificationLog.objects.filter(user=request.user)[:100]
    return render(request, "notifications/list.html", {"logs": logs})
