from django.db import models

from .ship import Ship
from .round import Round


class Fleet(models.Model):
    name = models.CharField(max_length=128)
    active = models.BooleanField(default=True)
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
        return Ship.objects.filter(fleet=self)
        
    @property
    def points(self):
        return sum(map(lambda e:e.points, self.ships))

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
        if self.task != "stand":
            raise ValueError("Cannot swap ships from a moving fleet")

        # Check if the other fleet is moving
        if other_fleet.task == "stand":
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
        
    def attack(self, turns, target):
        # Must raise ValueError when the fleet is already moving
        if self.task != "stand":
            raise ValueError("Fleet is already moving")

        # Must raise ValueError when the fleet's owner is protected
        if self.owner.is_protected:
            raise ValueError("The fleet's owner is protected")

        # Must raise ValueError when the turn calculations are running
        round = Round.objects.last()
        if round.calculate:
            raise ValueError("Turn calculation is running")
        
        # The fleet must contain ships
        if not self.ships.exists():
            raise ValueError("Fleet has no ships")
        
        # The target must be unprotected (define your logic here)
        if target.is_protected:
            raise ValueError("Target is protected and cannot be attacked")

        # The target cannot be an ally
        if target.is_ally(self.owner):
            raise ValueError("Target cannot be ally")

        # Must raise ValueError when the fleet's owner has no enough fuel
        fuel_cost = target.get_fuel_cost(self)
        if self.owner.narion < fuel_cost:
            raise ValueError("The fleet's owner has no enough fuel")            

        # Set the fleet's task to attack and assign the target
        self.task = "move"
        self.role = "Attackers"
        self.distance = target.get_distance(self)
        self.turns = turns
        self.target = target
        self.owner.narion -= fuel_cost
        self.save()
        
    def defend(self, turns, target):
        # Must raise ValueError when the fleet is already moving
        if self.task != "stand":
            raise ValueError("Fleet is already moving")
            
        # Must raise ValueError when the fleet's owner is protected
        if self.owner.is_protected:
            raise ValueError("The fleet's owner is protected")

        # Must raise ValueError when the turn calculations are running
        round = Round.objects.last()
        if round.calculate:
            raise ValueError("Turn calculation is running")

        # The fleet must contain ships
        if not self.ships.exists():
            raise ValueError("Fleet has no ships")
        
        # Must raise ValueError when the fleet's owner has no enough fuel
        fuel_cost = target.get_fuel_cost(self)
        if self.owner.narion < fuel_cost:
            raise ValueError("The fleet's owner has no enough fuel")            

        # Set the fleet's role to defend and assign the target
        self.task = "move"
        self.role = "Defenders"
        self.distance = target.get_distance(self)
        self.turns = turns
        self.target = target
        self.owner.narion -= fuel_cost
        self.save()
        
    def callback(self):
        # Prevent multiple use of callback
        if self.task == "return":
            raise ValueError("Fleet is already called back")
        
        # Must raise ValueError if the fleet is already at home
        if not self.target and self.task == "stand":
            raise ValueError("Fleet is already at home")
        
        # Must raise ValueError if the fleet is a base
        if self.base:
            raise ValueError("Base fleets cannot move or have a target")
        
        # Set the fleet's task to "return" and recount the distance
        self.task = "return"
        self.distance = self.target.get_distance(self) - self.distance

        # Recently started fleets has to return instantly
        if self.distance == 0:
            self.task = "stand"
            self.target = None
            self.distance = 0
            self.role = "Defenders"
        self.save()
            
    def tick(self):
        # Ensure the turn calculation is running
        round = Round.objects.last()
        if not round.calculate:
            raise ValueError("Turn calculation is not running")
        
        # Ensure the fleet is not a base
        if self.base:
            raise ValueError("Base fleets cannot move")

        # If no ships remain, return home instantly
        if not self.ships:
            self.task = "stand"
            self.target = None
            self.distance = 0
            self.role = "Defenders"
        
        # Decrease distance by 1
        if self.distance is not None:
            self.distance = max(0, self.distance - 1)
        
        if self.task == "move":
            if self.distance == 0:
                if self.turns is not None and self.turns > 0:
                    self.turns -= 1
                if self.turns == 0:
                    self.task = "return"
                    self.distance = self.target.get_distance(self)

        if self.task == "return":
            if self.distance == 0:
                # The fleet returns home
                self.task = "stand"
                self.target = None
                self.role = "Defenders"
                
        self.save()