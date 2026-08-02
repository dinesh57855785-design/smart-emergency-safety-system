from django.contrib import admin
from .models import SosEvent


@admin.register(SosEvent)
class SosEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'latitude', 'longitude')
    search_fields = ('user__username', 'message')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
