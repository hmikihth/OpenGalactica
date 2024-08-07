from django.db import models

from .ship import Ship


class Fleet(models.Model):
    name = models.CharField(max_length=128)
    base = models.BooleanField(default=False)
    owner = models.ForeignKey("Planet", on_delete=models.CASCADE, related_name="owner")
    formation = models.CharField(max_length=8, default="wall") # wedge, wall, sphere
    target = models.ForeignKey("Planet", on_delete=models.SET_NULL, related_name="target", null=True)
    distance = models.IntegerField(null=True)
    turns = models.IntegerField(null=True) # 1 to 3 for attackers, 1 to 6 for defenders
    task = models.CharField(max_length=8, null=True) # move, return, stand
    role = models.CharField(max_length=8, default="Defenders") # Defenders, Attackers

    @property
    def ships(self):
        return Ships.objects.filter(fleet=self)
    
    def add_ship(self, ship_model, quantity):
        Ship.objects.create(ship_model=ship_model, fleet=self, quantity=quantity)
