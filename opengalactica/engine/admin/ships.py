from django.contrib import admin
from engine.models import ShipModel, Ship


class ShipModelAdmin(admin.ModelAdmin):
    list_display = ["name", "species", "initiative"]
    ordering = ("name", "species", "initiative")
    
class ShipAdmin(admin.ModelAdmin):
    list_display = ["fleet", "ship_model", "quantity"]
    ordering = ("fleet", "ship_model", "quantity")


admin.site.register(ShipModel, ShipModelAdmin)
admin.site.register(Ship, ShipAdmin)
