#!/usr/bin/env python3

from engine.common import ROLES

class Battle:
    def __init__(self, attacking_fleets, defending_fleets):
        self.attacking_fleets = attacking_fleets
        self.defending_fleets = defending_fleets
#        for fleet in self.defending_fleets:
#            fleet.role = "Defenders"

    def get_all_ships(self):
        self.all_ships = [ship for fleet in self.attacking_fleets + self.defending_fleets for ship in fleet.ships]
        self.all_ships.sort(key=lambda x: x.initiative)

    def get_initiatives(self):
        self.initiatives = sorted(set(ship.initiative for ship in self.all_ships))

    def fire(self, firing_ships):
        total_damage = {}
        for target in firing_ships[0].target_order:
            for ship in firing_ships:
                print(  "\n### Firing:", ship.name, "Type", ship.weapon_type, "Initiative:", ship.initiative, ship.fleet.role, 
                        "Combat Ready:", ship.combat_ready)
                print("*** Hit:", ship.accuracy_points, "Weapons:", ship.weapon_count, "Damage",ship.damage)
                if ship.combat_ready <= 0:
                    continue

                if ship not in total_damage:
                    total_damage[ship] = ship.fire()
                
                enemy_ships = [s for s in self.all_ships if s.fleet.role != ship.fleet.role]
                print("\n---", target, total_damage[ship], "---")
                if not total_damage[ship] or target == "-":
                    continue
                target_ships = ship.select_target(target, enemy_ships)
                if not target_ships:
                    continue
                prev = total_damage[ship]
                for target_ship in target_ships:
                    total_damage[ship] = target_ship.hit(ship, target, total_damage[ship], target_ships)
                if ship.weapon_type == "blocker":
                    total_hp = sum(map(lambda e: (e.combat_ready-e.new_blocked-e.new_loss) * e.hp, target_ships))
                else:
                    total_hp = sum(map(lambda e: (e.remaining-e.new_loss) * e.hp, target_ships ))
                print("HP/S", total_hp, total_damage[ship])

            self.apply_hits(self.all_ships)
        
    def apply_hits(self, ships):
        for ship in ships:
            ship.apply_loss()
            ship.apply_steal()
            ship.apply_block()
            
    def calculate(self):
        self.get_all_ships()
        self.get_initiatives()

        print(self.initiatives)
        for initiative in self.initiatives:
            firing_ships = [ship for ship in self.all_ships if ship.initiative == initiative]
            self.fire(firing_ships)

    def print_battle_report(self):
        for role in ROLES:
            print(f"\n{role}:")
            print(f"{'Ship':<15} {'Initial':<8} {'Blocked':<8} {'Stolen':<8} {'Loss':<8}")
            ships = [ship for ship in self.all_ships if role == ship.fleet.role]
            for ship in ships:
                   print(f"{ship.name:<15} {ship.quantity:<8} {ship.blocked:<8} {ship.stolen:<8} {ship.loss:<8}")
