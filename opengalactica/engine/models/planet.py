MAX_FLEETS = 4

from django.db import models
from django.conf import settings

from .fleet import Fleet

from .alliance_member import AllianceMember
from .planet_economy import PlanetEconomy
from .planet_warfare import PlanetWarfare
from .planet_politics import PlanetPolitics

import os
import re
from django.utils.text import slugify

def sanitize_filename(filename):
    name, ext = os.path.splitext(filename)
    # Replace non-letter/digit characters with hyphens, keep extension
    name = re.sub(r'[^a-zA-Z0-9_-]', '-', name).strip('-')
    return f"{slugify(name)}{ext.lower()}"

def planet_profile_upload_path(instance, filename):
    filename = sanitize_filename(filename)
    return f"profiles/planet/{instance.id}/{filename}"

class Planet(models.Model, PlanetEconomy, PlanetWarfare, PlanetPolitics, AllianceMember):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    species =  models.CharField(max_length=32, null=True, blank=True, default=None)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    xp_before = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    points_before = models.IntegerField(default=0)

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
    
    profile_image = models.ImageField(upload_to=planet_profile_upload_path, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.coordinates})"
        
    def save(self, *args, **kwargs):
        is_new = self._state.adding  # Check if the object is being created

        if is_new:
            if self.x == self.y == self.z == 0:
                planets = Planet.objects.filter(x=0, y=0).values_list("z", flat=True)
                len_z = len(planets)
                if len_z:
                    max_z = max(planets)
                    if max_z == 9999:
                        self.z = [*filter(lambda e: e not in planets, range(1,10000))][0]
                    else:
                        self.z = max_z + 1
                else:
                    self.z = 1
                if len_z == 9999 and self.z == 0:
                    raise ValueError("The universe is full with planets")

        try:
            old_image = Planet.objects.get(pk=self.pk).profile_image
        except Planet.DoesNotExist:
            old_image = None

        obj = super().save(*args, **kwargs)
        
        if old_image and old_image != self.profile_image:
            if old_image.name and os.path.isfile(old_image.path):
                os.remove(old_image.path)
        
        if is_new:  # If it was a create call
            Fleet.objects.create(owner=self, name="Base", base=True)
            for i in range(MAX_FLEETS-1):
                Fleet.objects.create(owner=self, name=f"Fleet {i+1}")
            Fleet.objects.create(owner=self, name=f"Fleet {MAX_FLEETS}")
        return obj


    def delete(self, *args, **kwargs):
        if self.profile_image and os.path.isfile(self.profile_image.path):
            os.remove(self.profile_image.path)
        super().delete(*args, **kwargs)

    @property
    def coordinates(self):
        return f"{self.x}:{self.y}:{self.z}"
        
    @property
    def completed_researches(self):
        from .research import PlanetResearch
        return PlanetResearch.objects.filter(planet=self, completed=True)

    @property
    def satellites(self):
        from .satellite import StockedSatellite
        return StockedSatellite.objects.filter(planet=self)
                
    def recount_points(self):
        resource_points = (self.metal + self.crystal + self.narion) * 0.01
        plasmator_points = self.plasmators * 2500
        research_points = sum(map(lambda e:e.points, self.completed_researches))
        ship_points = sum(map(lambda e:e.points, self.fleets))
        satellite_points = sum(map(lambda e:e.points, self.satellites))
        
        self.points_before = self.points
        self.points = resource_points + plasmator_points + research_points + ship_points + satellite_points
        self.save()
