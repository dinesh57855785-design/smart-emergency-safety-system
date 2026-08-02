from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('api/daily_sos/', views.api_daily_sos, name='api_daily_sos'),
    path('api/monthly_sos/', views.api_monthly_sos, name='api_monthly_sos'),
    path('api/emergency_types/', views.api_emergency_types, name='api_emergency_types'),
    path('api/user_registrations/', views.api_user_registrations, name='api_user_registrations'),
]
