MAX_FLEETS = 4

from django.db import models
from django.conf import settings

from .fleet import Fleet

from .alliance_member import AllianceMember
from .planet_economy import PlanetEconomy
from .planet_warfare import PlanetWarfare
from .planet_politics import PlanetPolitics

class Planet(models.Model, PlanetEconomy, PlanetWarfare, PlanetPolitics, AllianceMember):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    r = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    metal_plasmator = models.IntegerField(default=1)
    crystal_plasmator = models.IntegerField(default=1)
    narion_plasmator = models.IntegerField(default=1)
    neutral_plasmator = models.IntegerField(default=0)

    metal = models.IntegerField(default=0)
    crystal = models.IntegerField(default=0)
    narion = models.IntegerField(default=0)

    credit = models.IntegerField(default=0)
    alliance = models.ForeignKey("Alliance", on_delete=models.SET_NULL, null=True, blank=True)
    rank = models.ForeignKey("AllianceRank", on_delete=models.SET_NULL, null=True, blank=True)
    protection = models.IntegerField(default=72)
    on_holiday = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.coordinates})"
        
    def save(self, *args, **kwargs):
        is_new = self._state.adding  # Check if the object is being created

        obj = super().save(*args, **kwargs)
        if is_new:  # If it was a create call
            Fleet.objects.create(owner=self, name="Base", base=True)
            for i in range(MAX_FLEETS-1):
                Fleet.objects.create(owner=self, name=f"Fleet {i+1}")
            Fleet.objects.create(owner=self, name=f"Fleet {MAX_FLEETS}")
        return obj

    @property
    def coordinates(self):
        return f"{self.r}:{self.x}:{self.y}:{self.z}"
                

