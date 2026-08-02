@@
     path('notifications/', include(('notifications.urls', 'notifications'), namespace='notifications')),
     path('police/', include(('police.urls', 'police'), namespace='police')),
+    path('video/', include(('video.urls', 'video'), namespace='video')),
     path('', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
 ]
