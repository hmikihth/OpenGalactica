from django.contrib import admin
from engine.models import Planet


class PlanetAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "coordinates"]
    ordering = ("name", "user")


admin.site.register(Planet, PlanetAdmin)