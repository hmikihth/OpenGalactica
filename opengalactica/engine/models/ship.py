from django.db import models

import random
from engine.common import FORMATIONS

class Species(models.Model):
    name = models.CharField(max_length=128)


class ShipModel(models.Model):
    name = models.CharField(max_length=128)
    pds = models.BooleanField(default=False)
    species =  models.CharField(max_length=32)
    ship_class =  models.CharField(max_length=8)
    target1 = models.CharField(max_length=8, default="-")
    target2 = models.CharField(max_length=8, default="-")
    target3 = models.CharField(max_length=8, default="-")
    weapon_type = models.CharField(max_length=16, default="std")
    initiative = models.IntegerField(default=0)
    evasion = models.IntegerField(default=0)
    weapon_count = models.IntegerField(default=0)
    accuracy_points = models.IntegerField(default=0)
    damage = models.IntegerField(default=0)
    hp = models.IntegerField(default=0)
    metal = models.IntegerField(default=0)
    crystal = models.IntegerField(default=0)
    narion = models.IntegerField(default=0)
    fuel = models.IntegerField(default=0)
    production_time = models.IntegerField(default=0)
    travel_sol = models.IntegerField(default=0)
    travel_gal = models.IntegerField(default=0)
    travel_uni = models.IntegerField(default=0)
    requirement = models.ForeignKey('Research', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

    @property
    def cost(self):
        return self.metal + self.crystal + self.narion
        
    @property
    def points(self):
        return self.cost * 0.1
        
    def can_produce(self, planet):
        if self.species == "Extra":
            return True #TODO: check active extra
        # TODO: check tech requirements
        return self.species == planet.species

class ShipProto():
    loss = 0
    blocked = 0
    stolen = 0
    new_loss = 0
    new_blocked = 0
    new_stolen = 0
    remaining = 0
    combat_ready = 0
    
    @property
    def name(self):
        return self.ship_model.name
    
    @property
    def species(self):
        return self.ship_model.species
    
    @property
    def ship_class(self):
        return self.ship_model.ship_class
    
    @property
    def target1(self):
        return self.ship_model.target1
    
    @property
    def target2(self):
        return self.ship_model.target2
    
    @property
    def target3(self):
        return self.ship_model.target3
    
    @property
    def initiative(self):
        return self.ship_model.initiative
    
    @property
    def weapon_type(self):
        return self.ship_model.weapon_type
        
    @property
    def evasion(self):
        return self.ship_model.evasion
        
    @property
    def weapon_count(self):
        return self.ship_model.weapon_count
        
    @property
    def accuracy_points(self):
        return self.ship_model.accuracy_points
        
    @property
    def damage(self):
        return self.ship_model.damage
        
    @property
    def hp(self):
        return self.ship_model.hp
        
    @property
    def metal(self):
        return self.ship_model.metal
        
    @property
    def crystal(self):
        return self.ship_model.crystal
        
    @property
    def narion(self):
        return self.ship_model.narion

    @property
    def cost(self):
        return self.ship_model.cost 

    @property
    def points(self):
        return self.ship_model.points * self.quantity
        
    @property
    def target_order(self):
        return (self.target1, self.target2, self.target3)

    @property
    def travel_sol(self):
        return self.ship_model.travel_sol

    @property
    def travel_gal(self):
        return self.ship_model.travel_gal

    @property
    def travel_uni(self):
        return self.ship_model.travel_uni

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value
        self.remaining = value
        self.combat_ready = value
        
    def hit_standard(self, damage, accuracy):
        loss = min(self.remaining, int(damage*accuracy // self.hp))
        if self.loss + self.new_loss + loss > self.quantity:
            loss = self.quantity - self.loss - self.new_loss
        if loss + self.new_loss + self.loss + self.blocked > self.quantity:
            self.new_blocked += self.quantity - (loss + self.new_loss + self.loss + self.blocked)
        self.new_loss += loss
        return (loss * self.hp) // accuracy
        
    def hit_block(self, damage, accuracy):
        block = min(self.combat_ready, int(damage*accuracy // self.hp))
        if self.loss + self.blocked + self.new_blocked + block > self.quantity:
            block = self.quantity - self.loss - self.blocked - self.new_blocked
        self.new_blocked += block
        return (block * self.hp) // accuracy

    def hit_steal(self, damage):
        loss = min((self.remaining - self.new_loss) // 2 - self.new_stolen, damage // self.hp)
        self.new_stolen += loss // 2
        return loss * self.hp

    def apply_loss(self):
        self.loss += self.new_loss
        self.remaining -= self.new_loss
        self.combat_ready -= self.new_loss
        self.new_loss = 0

    def apply_steal(self):
        self.stolen += self.new_stolen
        self.new_stolen = 0

    def apply_block(self):
        self.blocked += self.new_blocked
        self.combat_ready -= self.new_blocked
        self.new_blocked = 0
        
    def hit(self, firing_ship, target, total_damage, target_ships):
        if firing_ship.weapon_type == "blocker":
            if not self.combat_ready:
                return total_damage
            quantity = self.combat_ready - self.new_blocked * (self.name != firing_ship.name)
            total_quantity = sum(map(lambda e:e.combat_ready, target_ships))
            total_cost = sum(map(lambda e:e.combat_ready*e.cost, target_ships))
        else:
            if not self.remaining:
                return total_damage
            quantity = self.remaining - self.new_loss * (self.name != firing_ship.name)
            total_quantity = sum(map(lambda e:e.remaining, target_ships))
            total_cost = sum(map(lambda e:e.remaining*e.cost, target_ships))
            
        if target == "All":
            ratio = quantity * self.cost / total_cost
        else:
            ratio = quantity / total_quantity

        if not ratio:
            return total_damage
            
        evasion_points = self.evasion * (100 + FORMATIONS[self.fleet.formation][0]) / 100

        accuracy_bonus = FORMATIONS[firing_ship.fleet.formation][1]
        accuracy_points = firing_ship.accuracy_points * (100 + accuracy_bonus + firing_ship.fleet.rank) / 100 
        accuracy = (accuracy_points - evasion_points)/100

        damage = int(total_damage * ratio)

        if firing_ship.weapon_type == "blocker":
            d = self.hit_block(damage, accuracy)
            total_damage -= d
        else:
            d = self.hit_standard(damage, accuracy)
            total_damage -= d
            if firing_ship.weapon_type == "thief":
                d = self.hit_steal(int(d*accuracy))
        return total_damage

    def select_target(self, target, ships):
        if self.weapon_type == "blocker":
            if target == "All":
                return [ship for ship in ships if ship.combat_ready > 0]
            else:
                return [ship for ship in ships if ship.ship_class == target and ship.combat_ready > 0]
        else:
            if target == "All":
                return [ship for ship in ships if ship.remaining > 0]
            else:
                return [ship for ship in ships if ship.ship_class == target and ship.remaining > 0]

    def fire(self):
        total_damage = self.combat_ready * self.weapon_count * self.damage * random.uniform(0.98, 1.02)
        return total_damage


class Ship(models.Model, ShipProto):
    ship_model = models.ForeignKey("ShipModel", on_delete=models.CASCADE)
    fleet =  models.ForeignKey("Fleet", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
        
    @property
    def fuel_cost(self):
        return self.ship_model.fuel * self.quantity

    def scrap(self, quantity):
        if quantity > self.quantity:
            raise ValueError("Not enough ships to scrap")

        self.quantity -= quantity
        self.save(update_fields=['quantity'])

        ship_model = self.ship_model
        planet = self.fleet.owner

        metal = int(ship_model.metal * quantity * 0.5)
        crystal = int(ship_model.crystal * quantity * 0.5)
        narion = int(ship_model.narion * quantity * 0.5)
        
        planet.metal += metal
        planet.crystal += crystal
        planet.narion += narion
        planet.save(update_fields=['metal', 'crystal', 'narion'])

        return {
            'metal': metal,
            'crystal': crystal,
            'narion': narion,
        }
    
class ShipProduction(models.Model):
    planet = models.ForeignKey("Planet", on_delete=models.CASCADE)
    ship_model = models.ForeignKey("ShipModel", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    turns_remaining = models.IntegerField()  # Production time remaining

    def save(self, *args, **kwargs):
        total_metal_cost = self.ship_model.metal * self.quantity
        total_crystal_cost = self.ship_model.crystal * self.quantity
        total_narion_cost = self.ship_model.narion * self.quantity

        # Check if the planet has enough resources
        if (self.planet.metal < total_metal_cost or 
            self.planet.crystal < total_crystal_cost or 
            self.planet.narion < total_narion_cost):
            raise ValueError("Not enough resources to produce the ships.")
        else:
            # Deduct the resources from the planet
            self.planet.metal -= total_metal_cost
            self.planet.crystal -= total_crystal_cost
            self.planet.narion -= total_narion_cost
            self.planet.save()  # Save the planet after deducting resources

        if self.turns_remaining is None:
            self.turns_remaining = self.ship_model.production_time
        return super().save(*args, **kwargs)

    def start_production(self):
        """Start or continue ship production."""
        if self.turns_remaining > 0:
            self.turns_remaining -= 1
            if self.turns_remaining <= 0:
                from .fleet import Fleet
                fleet, _ = Fleet.objects.get_or_create(owner=self.planet, base=True)
                stock, _ = Ship.objects.get_or_create(fleet=fleet, ship_model=self.ship_model)
                stock.quantity += self.quantity
                stock.save()
                self.delete()
                return True
            self.save()

    def __str__(self):
        return f"{self.planet} - {self.ship_model.name} (Turns left: {self.turns_remaining})"
    