import random

from django.db import models
from django.conf import settings

from .ship import Ship, ShipModel
from .fleet import Fleet

class Market:
    metal = models.IntegerField(default=1000000)
    crystal = models.IntegerField(default=1000000)
    narion = models.IntegerField(default=1000000)

    metal_rate = models.FloatField(default=0.6)
    crystal_rate = models.FloatField(default=0.5)
    narion_rate = models.FloatField(default=0.4)

class PlanetEconomy:
    @property
    def active_plasmators(self):
        return self.metal_plasmator + self.crystal_plasmator + self.narion_plasmator
        
    @property
    def plasmators(self):
        return self.active_plasmators + self.neutral_plasmator

    @property
    def production_minister_bonus(self):
        return 1 + (0.1 * self.is_minister)
        
    @property
    def plasmator_production(self):
        if self.active_plasmators < 100:
            return 500
        elif self.active_plasmators > 1000:
            return 400
        else:
            return 510 - (11*self.active_plasmators)//100

    @property
    def tax_rate(self):
        if self.alliance:
            return self.alliance.tax_rate
        return 0

    @property
    def metal_capacity(self):
        # NOTE: Later implement resource based capacity
        return 30000000

    @property
    def crystal_capacity(self):
        # NOTE: Later implement resource based capacity
        return 30000000

    @property
    def narion_capacity(self):
        # NOTE: Later implement resource based capacity
        return 30000000

    @property
    def planet_metal_production(self):
        # Note: Later implement research and species specific productions!
        return 1000

    @property
    def planet_crystal_production(self):
        # Note: Later implement research and species specific productions!
        return 1000

    @property
    def planet_narion_production(self):
        # Note: Later implement research and species specific productions!
        return 1000

    @property
    def gross_metal_production(self):
        metal = self.planet_metal_production + self.metal_plasmator * self.plasmator_production
        metal *= self.production_minister_bonus
        return metal

    @property
    def gross_crystal_production(self):
        crystal = self.planet_crystal_production + self.crystal_plasmator * self.plasmator_production
        crystal *= self.production_minister_bonus
        return crystal

    @property
    def gross_narion_production(self):
        narion = self.planet_narion_production + self.narion_plasmator * self.plasmator_production
        narion *= self.production_minister_bonus
        return narion

    @property
    def metal_tax(self):
        return int(self.gross_metal_production * self.tax_rate)

    @property
    def crystal_tax(self):
        return int(self.gross_crystal_production * self.tax_rate)

    @property
    def narion_tax(self):
        return int(self.gross_narion_production * self.tax_rate)

    @property
    def net_metal_production(self):
        return self.gross_metal_production - self.metal_tax

    @property
    def net_crystal_production(self):
        return self.gross_crystal_production - self.crystal_tax

    @property
    def net_narion_production(self):
        return self.gross_narion_production - self.narion_tax

    def generate_resources(self):
        self.metal = min(self.metal_capacity, self.metal + self.net_metal_production)
        self.crystal = min(self.crystal_capacity, self.crystal + self.net_crystal_production)
        self.narion = min(self.narion_capacity, self.narion + self.net_narion_production)
        self.pay_taxes()
        
    def pay_taxes(self, metal, crystal, narion):
        self.alliance.pay_taxes(self, self.metal_tax, self.crystal_tax, self.narion_tax)
        
    def exchange(self, input, output, amount):
        market = Market.objects.first()
        rate = {"metal":market.metal_rate, "crystal":market.crystal_rate, "narion":market.narion_rate}
        
        if input not in rate:
            raise ValueError("Input resource type does not exist!")
        if output not in rate:
            raise ValueError("Output resource type does not exist!")
        
        amount = min(amount, self.__dict__[input])
        output_amount = min(amount * rate[input], market.__dict__[output])
        
        market.__dict__[input] += amount
        market.__dict__[output] -= output_amount
        market.save()

        self.__dict__[input] -= amount
        self.__dict__[output] += output_amount        
        self.save()



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


class PlanetPolitics:
    @property
    def galaxy(self):
        from .galaxy import Galaxy
        return Galaxy.objects.get(r=self.r, x=self.x, y=self.y)
    
    @property
    def is_minister(self):
        return self in (self.galaxy.commander, self.galaxy.minister_of_war)
                                
    def relocation(self):
        pass


class Planet(models.Model, PlanetEconomy, PlanetWarfare, PlanetPolitics):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    r = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    tp = models.IntegerField(default=0)
    point = models.IntegerField(default=0)

    metal_plasmator = models.IntegerField(default=1)
    crystal_plasmator = models.IntegerField(default=1)
    narion_plasmator = models.IntegerField(default=1)
    neutral_plasmator = models.IntegerField(default=0)

    metal = models.IntegerField(default=0)
    crystal = models.IntegerField(default=0)
    narion = models.IntegerField(default=0)

    credit = models.IntegerField(default=0)
    alliance = models.ForeignKey("Alliance", on_delete=models.SET_NULL, null=True, blank=True)
    protection = models.IntegerField(default=72)
    on_holiday = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.coordinates})"

    @property
    def coordinates(self):
        return f"{self.r}:{self.x}:{self.y}:{self.z}"
                

class PlanetRelocation(models.Model):
    planet = models.ForeignKey("Planet", on_delete=models.CASCADE, null=True, blank=True)
    turn = models.IntegerField(default=0)
    r = models.IntegerField(default=None, null=True, blank=True)
    x = models.IntegerField(default=None, null=True, blank=True)
    y = models.IntegerField(default=None, null=True, blank=True)
    z = models.IntegerField(default=None, null=True, blank=True)

    def execute(self):
        if self.r == None:
            pass
        if self.x == None:
            pass