from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('profiles/', include(('profiles.urls', 'profiles'), namespace='profiles')),
    path('contacts/', include(('contacts.urls', 'contacts'), namespace='contacts')),
    path('sos/', include(('sos.urls', 'sos'), namespace='sos')),
    path('location/', include(('location.urls', 'location'), namespace='location')),
    path('voice/', include(('voice.urls', 'voice'), namespace='voice')),
+    path('notifications/', include(('notifications.urls', 'notifications'), namespace='notifications')),
    path('', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
