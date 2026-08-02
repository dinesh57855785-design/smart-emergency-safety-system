from django.contrib import admin
from .models import ReportExport


@admin.register(ReportExport)
class ReportExportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'file_type', 'user', 'created_at', 'record_count')
    list_filter = ('report_type', 'file_type', 'created_at')
    search_fields = ('user__username',)
