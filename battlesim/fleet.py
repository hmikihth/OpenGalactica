#!/usr/bin/env python3

class Fleet:
    def __init__(self, name, formation="wall", rank=0):
        self.name = name
        self.formation = formation
        self.ships = []
        self.rank = rank
        self.role = "Attackers"

    def add_ship(self, ship, quantity):
        s = ship.copy()
        s.set_quantity(quantity)
        s.fleet = self
        self.ships.append(s)
