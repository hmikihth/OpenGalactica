from django.contrib import admin
from engine.models import Alliance


class AllianceAdmin(admin.ModelAdmin):
    list_display = ["name", "news"]
    ordering = ("name",)


admin.site.register(Alliance, AllianceAdmin)