from django.contrib import admin
from engine.models import PlanetResearch


class PlanetResearchAdmin(admin.ModelAdmin):
    list_display = ["planet", "research", ]


admin.site.register(PlanetResearch, PlanetResearchAdmin)