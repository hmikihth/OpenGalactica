from django.contrib import admin
from engine.models import ShipModel


class ShipModelAdmin(admin.ModelAdmin):
    list_display = ["name", "species", "initiative"]
    ordering = ("name", "species", "initiative")


admin.site.register(ShipModel, ShipModelAdmin)