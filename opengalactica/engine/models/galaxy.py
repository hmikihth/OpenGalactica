from django.db import models

from .planet import Planet

class Galaxy(models.Model):
    name = models.CharField(max_length=128)
    commander = models.ForeignKey("Planet", related_name="commander", on_delete=models.SET_NULL, null=True, blank=True)
    minister_of_war = models.ForeignKey("Planet", related_name="minister_of_war", on_delete=models.SET_NULL, null=True, blank=True)
    r = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    @property
    def planets(self):
        return Planet.objects.filter(r=self.r, x=self.x, y=self.y).order_by("z")
        
    @property
    def full(self):
        return len(self.planets) > 9
            
    def add_planet(self, planet):
        if not self.full:
            busy = Planet.objects.filter(r=self.r, x=self.x, y=self.y).values_list("z", flat=True)
            z = random.choice([*filter(lambda e: e not in busy, range(1,11))])
        else:
            raise ValueError("The galaxy is full")
        
    def relocate_into(self, r_req):
        if not self.full:
            existing_planet = Planet.objects.filter(r=self.r, x=self.x, y=self.y, z=r_req.z)
            if existing_planet:
                raise ValueError("There is a planet on the given coordinates")
            else:
                planet = r_req.planet
                planet.r = self.r
                planet.x = self.x
                planet.y = self.y
                planet.z = r_req.z
                planet.save()
                r_req.delete()
        else:
            raise ValueError("The galaxy is full")
