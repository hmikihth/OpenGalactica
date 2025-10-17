from django.contrib import admin
from engine.models import ShipModel, Ship, ShipProduction


class ShipModelAdmin(admin.ModelAdmin):
    list_display = ["name", "species", "initiative"]
    ordering = ("name", "species", "initiative")
    
class ShipAdmin(admin.ModelAdmin):
    list_display = ["fleet", "ship_model", "quantity"]
    ordering = ("fleet", "ship_model", "quantity")

class ShipProductionAdmin(admin.ModelAdmin):
    list_display = ["planet", "ship_model", "turns_remaining", "quantity"]
    ordering = ("planet", "ship_model", "turns_remaining", "quantity")


admin.site.register(ShipModel, ShipModelAdmin)
admin.site.register(ShipProduction, ShipProductionAdmin)
admin.site.register(Ship, ShipAdmin)
