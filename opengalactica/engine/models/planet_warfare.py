from .ship import Ship
from .fleet import Fleet

class PlanetWarfare:
    @property
    def fleets(self):
        return Fleet.objects.filter(owner=self).order_by("-base","id")

    @property
    def base(self):
        return Fleet.objects.get(owner=self, base=True)

    @property
    def n_ships(self):
        return sum(map(lambda e:e.n_ships, self.fleets))
    
    @property
    def n_pds(self):
        return self.base.n_pds
    
    @property
    def is_protected(self):
        return self.protection > 0 or self.on_holiday

    @property
    def defenders(self):
        return [*Fleet.objects.filter(target=self, distance=0, role="Defenders")]    

    @property
    def attackers(self):
        return [*Fleet.objects.filter(target=self, distance=0, role="Attackers")]
        
    @property
    def fleets_on_base(self):
        return [*Fleet.objects.filter(owner=self, distance=0, task="stand")]

    @property
    def incoming_fleets(self):
        return [*Fleet.objects.filter(target=self, task="move")]

    @property
    def outgoing_fleets(self):
        return [*Fleet.objects.filter(owner=self, task="move")]

    @property
    def returning_fleets(self):
        return [*Fleet.objects.filter(owner=self, task="return")]

    def is_ally(self, other):
        same_sol = (self.x == other.x and self.y == other.y)
        same_alliance = self.alliance and (self.alliance == other.alliance)
        return same_sol or same_alliance

    def get_distance(self, fleet):
        other = fleet.owner
        travel = "travel_uni"
        if self.x == other.x:
            travel = "travel_gal"
            if self.y == other.y:
                travel = "travel_sol"
                    
        ships = Ship.objects.filter(fleet=fleet)
        if ships:
            return max(map(lambda e:e.ship_model.__dict__[travel], ships))

    def get_fuel_cost(self, fleet):
        other = fleet.owner
        multiplier = 3
        if self.x == other.x:
            multiplier = 2
            if self.y == other.y:
                multiplier = 1
        return fleet.fuel_cost * multiplier
                    
    def battle(self):
        from engine.common import Battle
        battle = Battle(self.attackers, self.defenders + self.fleets_on_base)
        battle.calculate()
