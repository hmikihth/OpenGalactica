from django.db import models

from .ship import Ship
from .round import Round


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
        # Must raise ValueError when the turn calculations are running
        round = Round.objects.last()
        if round.calculate:
            raise ValueError("Turn calculation is running")

        if quantity > 0:
            ship, created = Ship.objects.get_or_create(ship_model=ship_model, fleet=self)
            ship.quantity += quantity
            ship.save()
        else:
            raise ValueError("Quantity must be positive")


    def swap_ship(self, other_fleet, ship_model, quantity):
        # Must raise ValueError when the turn calculations are running
        round = Round.objects.last()
        if round.calculate:
            raise ValueError("Turn calculation is running")
        
        # Check the owners
        if self.owner != other_fleet.owner:
            raise ValueError("Fleets must have the same owner")
        
        # Check if the quantity is positive
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer")

        # Check if the current fleet is moving
        if self.task == "move":
            raise ValueError("Cannot swap ships from a moving fleet")

        # Check if the other fleet is moving
        if other_fleet.task == "move":
            raise ValueError("Cannot swap ships to a moving fleet")

        # Get the ship from the current fleet
        ship = Ship.objects.filter(fleet=self, ship_model=ship_model).first()
        if not ship or ship.quantity < quantity:
            raise ValueError("Not enough ships to swap")

        # Deduct the quantity from the current fleet
        ship.quantity -= quantity
        if ship.quantity == 0:
            ship.delete()
        else:
            ship.save()

        # Add the quantity to the other fleet
        other_ship, created = Ship.objects.get_or_create(fleet=other_fleet, ship_model=ship_model)
        other_ship.quantity += quantity
        other_ship.save()
        
    def attack(self, turns):
        pass
        
    def defend(self, turns):
        pass
        
    def callback(self):
        pass

    def tick(self):
        pass
