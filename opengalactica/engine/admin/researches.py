from django.contrib import admin
from engine.models import Research


class ResearchAdmin(admin.ModelAdmin):
    list_display = ["name",]


admin.site.register(Research, ResearchAdmin)