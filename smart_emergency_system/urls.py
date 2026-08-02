@@
     path('voice/', include(('voice.urls', 'voice'), namespace='voice')),
     path('notifications/', include(('notifications.urls', 'notifications'), namespace='notifications')),
+    path('police/', include(('police.urls', 'police'), namespace='police')),
     path('', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
 ]
