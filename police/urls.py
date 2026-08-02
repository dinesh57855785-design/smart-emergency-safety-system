from django.urls import path
from . import views

urlpatterns = [
    path('notify/', views.notify, name='notify'),
    # manual page
    path('manual/', views.notify_page, name='notify_page'),
]
