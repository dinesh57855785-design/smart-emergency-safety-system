from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/daily/', views.api_daily, name='api_daily'),
    path('api/weekly/', views.api_weekly, name='api_weekly'),
    path('api/monthly/', views.api_monthly, name='api_monthly'),
    path('api/user_activity/', views.api_user_activity, name='api_user_activity'),
    path('api/emergency_types/', views.api_emergency_types, name='api_emergency_types'),
    path('api/police_stats/', views.api_police_stats, name='api_police_stats'),
    path('api/sms_stats/', views.api_sms_stats, name='api_sms_stats'),
    path('api/video_stats/', views.api_video_stats, name='api_video_stats'),
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
]
