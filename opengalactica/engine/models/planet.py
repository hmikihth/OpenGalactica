from django.db import models
from django.conf import settings

from .ship import Ship, ShipModel

class Planet(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    r = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    tp = models.IntegerField(default=0)
    point = models.IntegerField(default=0)
    metal = models.IntegerField(default=0)
    crystal = models.IntegerField(default=0)
    narion = models.IntegerField(default=0)
    credit = models.IntegerField(default=0)
    alliance = models.ForeignKey("Alliance", on_delete=models.SET_NULL, null=True, blank=True)
    protection = models.IntegerField(default=72)

    @property
    def coordinates(self):
        return f"{self.r}:{self.x}:{self.y}:{self.z}"
        
    def __str__(self):
        return f"{self.name} ({self.coordinates})"
        
    def is_protected(self):
        return self.protection > 0
        
    def is_ally(self, other):
        same_galaxy = (self.r == other.r and self.x == other.x and self.y == other.y)
        same_alliance = self.alliance and (self.alliance == other.alliance)
        return same_galaxy or same_alliance

    def get_distance(self, fleet):
        other = fleet.owner
        travel = "travel_u"
        if self.r == other.r and self.x == other.x:
            travel = "travel_s"
            if self.y == other.y:
                travel = "travel_g"
                    
        ships = Ship.objects.filter(fleet=fleet)
        return max(map(lambda e:e.ship_model.__dict__[travel], ships))
