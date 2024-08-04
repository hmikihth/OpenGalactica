#!/usr/bin/env python3

import random
from .common import FORMATIONS

class Ship:
    def __init__(self, name, species, ship_class, target_order, weapon_type, initiative, evasion, weapon_count, 
                accuracy_points, damage, hp, metal, crystal, narion, fleet=None):
        self.name = name
        self.species = species
        self.ship_class = ship_class
        if type(target_order) == str:
            self.target_order = target_order.split()
        else:
            self.target_order = target_order
        self.weapon_type = weapon_type
        self.initiative = initiative
        self.evasion = evasion
        self.weapon_count = weapon_count
        self.accuracy_points = accuracy_points
        self.damage = damage
        self.hp = hp
        self.metal = metal
        self.crystal = crystal
        self.narion = narion
        
        self.loss = 0
        self.blocked = 0
        self.stolen = 0
        self.new_loss = 0
        self.new_blocked = 0
        self.new_stolen = 0
        self.fleet = fleet
        self.cost = sum((metal, crystal, narion))
        
    def set_quantity(self, quantity):
        self.quantity = quantity
        self.remaining = quantity
        self.combat_ready = quantity

        
    def copy(self):
        return Ship(self.name, self.species, self.ship_class, self.target_order, self.weapon_type, 
                    self.initiative, self.evasion, self.weapon_count, self.accuracy_points, 
                    self.damage, self.hp, self.metal, self.crystal, self.narion)

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
            
        evasion_points = self.evasion * (100 + TIONS[self.fleet.formation][0]) / 100

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
