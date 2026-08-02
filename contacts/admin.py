from django.contrib import admin
from .models import EmergencyContact


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'relationship', 'created_at')
    search_fields = ('user__username', 'name', 'phone')
    list_filter = ('relationship', 'created_at')
    ordering = ('-created_at',)
