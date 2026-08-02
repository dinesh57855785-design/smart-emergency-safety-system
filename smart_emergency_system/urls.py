@@
     path('notifications/', include(('notifications.urls', 'notifications'), namespace='notifications')),
     path('police/', include(('police.urls', 'police'), namespace='police')),
     path('video/', include(('video.urls', 'video'), namespace='video')),
+    path('reports/', include(('reports.urls', 'reports'), namespace='reports')),
     path('', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
 ]
