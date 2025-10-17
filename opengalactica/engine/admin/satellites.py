from django.contrib import admin
from engine.models import SatelliteType, StockedSatellite, SatelliteProduction, ProbeReport


class SatelliteTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "metal", "crystal", "narion", "production_time", 
                    "requires_rocket", "rocket_required_count", "requirement"]
    ordering = ("production_time", "name")
    
class StockedSatelliteAdmin(admin.ModelAdmin):
    list_display = ["planet", "satellite_type", "quantity"]
    ordering = ("planet",)

class SatelliteProductionAdmin(admin.ModelAdmin):
    list_display = ["planet", "satellite_type", "turns_remaining", "quantity"]
    ordering = ("planet", "satellite_type", "turns_remaining", "quantity")

class ProbeReportAdmin(admin.ModelAdmin):
    list_display = ["id", "server_time", "sender_planet", "target_planet"]
    ordering = ("-id", "server_time", "sender_planet", "target_planet")


admin.site.register(SatelliteType, SatelliteTypeAdmin)
admin.site.register(StockedSatellite, StockedSatelliteAdmin)
admin.site.register(SatelliteProduction, SatelliteProductionAdmin)
admin.site.register(ProbeReport, ProbeReportAdmin)
