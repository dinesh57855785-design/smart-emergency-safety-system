from django.contrib import admin
from .models import SosEvent


@admin.register(SosEvent)
class SosEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'message')
