from .ship import Ship
from .fleet import Fleet

class PlanetWarfare:
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
        same_galaxy = (self.r == other.r and self.x == other.x and self.y == other.y)
        same_alliance = self.alliance and (self.alliance == other.alliance)
        return same_galaxy or same_alliance

    def get_distance(self, fleet):
        other = fleet.owner
        travel = "travel_u"
        if self.r == other.r and self.x == other.x:
            travel = "travel_s"
            if self.y == other.y:
                travel = "travel_g"
                    
        ships = Ship.objects.filter(fleet=fleet)
        if ships:
            return max(map(lambda e:e.ship_model.__dict__[travel], ships))

    def get_fuel_cost(self, fleet):
        other = fleet.owner
        multiplier = 3
        if self.r == other.r and self.x == other.x:
            multiplier = 2
            if self.y == other.y:
                multiplier = 1
                    
        ships = Ship.objects.filter(fleet=fleet)
        return sum(map(lambda e: e.fuel_cost * multiplier,  ships))

    def battle(self):
        from engine.common import Battle
        battle = Battle(self.attackers, self.defenders + self.fleets_on_base)
        battle.calculate()
