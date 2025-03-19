from django.contrib import admin
from engine.models import Sol


class SolAdmin(admin.ModelAdmin):
    list_display = ["name", "x", "y", "commander", "minister_of_war"]
    ordering = ("x", "y")


admin.site.register(Sol, SolAdmin)