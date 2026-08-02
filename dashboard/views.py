from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from notifications.models import SMSNotification


@login_required
def index(request):
    # show recent SMS notifications related to user
    notifications = SMSNotification.objects.filter(sos_event__user=request.user)[:10]
    return render(request, 'dashboard/index.html', {'notifications': notifications})
