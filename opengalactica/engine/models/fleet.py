from django.db import models

from .ship import Ship


class Fleet(models.Model):
    name = models.CharField(max_length=128)
    base = models.BooleanField(default=False)
    owner = models.ForeignKey("Planet", on_delete=models.CASCADE, related_name="owner")
    formation = models.CharField(max_length=16, default="wall") # wedge, wall, sphere
    target = models.ForeignKey("Planet", on_delete=models.SET_NULL, related_name="target", null=True, blank=True)
    distance = models.IntegerField(null=True, blank=True)
    turns = models.IntegerField(null=True, blank=True) # 1 to 3 for attackers, 1 to 6 for defenders
    task = models.CharField(max_length=16, null=True, blank=True) # move, return, stand
    role = models.CharField(max_length=16, default="Defenders", null=True, blank=True) # Defenders, Attackers

    @property
    def ships(self):
        return Ships.objects.filter(fleet=self)

    def __str__(self):
        return f"{self.name} - {self.owner.name} ({self.owner.coordinates})"
    
    def add_ship(self, ship_model, quantity):
        if quantity > 0:
            ship, created = Ship.objects.get_or_create(ship_model=ship_model, fleet=self)
            ship.quantity += quantity
            ship.save()
        else:
            raise ValueError("Quantity must be positive")

    def swap_ship(self, other_fleet, quantity):
        pass
        
    def attack(self, turns):
        pass
        
    def defend(self, turns):
        pass
        
    def callback(self):
        pass

    def tick(self):
        pass
