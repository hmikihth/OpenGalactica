from django.db import models

import random
from engine.common import FORMATIONS

class Species(models.Model):
    name = models.CharField(max_length=128)


class ShipClass(models.Model):
    name = models.CharField(max_length=128)
    identifier = models.CharField(max_length=6)


class ShipModel(models.Model):
    name = models.CharField(max_length=128)
    species =  models.ForeignKey("Species", on_delete=models.SET_NULL, null=True)
    ship_class =  models.ForeignKey("ShipClass", on_delete=models.SET_NULL, null=True)
    target1 = models.CharField(max_length=8, default="-")
    target2 = models.CharField(max_length=8, default="-")
    target3 = models.CharField(max_length=8, default="-")
    weapon_type = models.CharField(max_length=8, default="std")
    initiative = models.IntegerField(default=0)
    evasion = models.IntegerField(default=0)
    weapon_count = models.IntegerField(default=0)
    accuracy_points = models.IntegerField(default=0)
    damage = models.IntegerField(default=0)
    hp = models.IntegerField(default=0)
    metal = models.IntegerField(default=0)
    crystal = models.IntegerField(default=0)
    narion = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    

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
    def target_order(self):
        return (self.target1, self.target2, self.target3)

    @property
    def quantity(self):
        return self._quantity

    @property.setter
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
        print(  self.name, "Evasion:", self.evasion, "HP:", self.hp, "Ratio:", round(ratio,2), "Quantity:", self.quantity, "R:", self.remaining, 
                "C:", self.combat_ready, "NL:",self.new_loss,"NB:", self.new_blocked)
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


class Ship(ShipClass, ShipProto):
    ship_model = models.ForeignKey("ShipModel", on_delete=models.CASCADE)
    fleet =  models.ForeignKey("Fleet", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    
    