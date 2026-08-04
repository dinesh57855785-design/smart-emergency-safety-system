from django.contrib import admin
from .models import FaceProfile


@admin.register(FaceProfile)
class FaceProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at")
    search_fields = ("user__email", "user__username")
    readonly_fields = ("descriptor", "created_at", "updated_at")
