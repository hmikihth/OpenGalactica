from django.contrib import admin
from engine.models import Fleet


class FleetAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "target", "distance", "base", "role"]
    ordering = ("name", "owner", "target")


admin.site.register(Fleet, FleetAdmin)
