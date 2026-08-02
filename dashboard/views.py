@@
 from notifications.models import SMSNotification
 from police.models import PoliceNotification
+from video.models import VideoSession
@@
-    notifications = SMSNotification.objects.filter(sos_event__user=request.user)[:10]
-    police_notifications = PoliceNotification.objects.filter(sos_event__user=request.user)[:10]
-    return render(request, 'dashboard/index.html', {'notifications': notifications, 'police_notifications': police_notifications})
+    notifications = SMSNotification.objects.filter(sos_event__user=request.user)[:10]
+    police_notifications = PoliceNotification.objects.filter(sos_event__user=request.user)[:10]
+    video_sessions = VideoSession.objects.filter(sos_event__user=request.user, status='active')[:5]
+    return render(request, 'dashboard/index.html', {'notifications': notifications, 'police_notifications': police_notifications, 'video_sessions': video_sessions})
