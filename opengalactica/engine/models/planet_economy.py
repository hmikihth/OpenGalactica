from django.db import models

class Market(models.Model):
    metal = models.IntegerField(default=1000000)
    crystal = models.IntegerField(default=1000000)
    narion = models.IntegerField(default=1000000)

    metal_rate = models.FloatField(default=0.6)
    crystal_rate = models.FloatField(default=0.5)
    narion_rate = models.FloatField(default=0.4)

class PlanetEconomy:
    @property
    def construction_count(self):
        return len(self.completed_researches.filter(research__building=False))

    @property
    def development_count(self):
        return len(self.completed_researches.filter(research__building=True))

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
        # NOTE: Later implement research based capacity
        return 30000000

    @property
    def crystal_capacity(self):
        # NOTE: Later implement research based capacity
        return 30000000

    @property
    def narion_capacity(self):
        # NOTE: Later implement research based capacity
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
        return int(metal)

    @property
    def gross_crystal_production(self):
        crystal = self.planet_crystal_production + self.crystal_plasmator * self.plasmator_production
        crystal *= self.production_minister_bonus
        return int(crystal)

    @property
    def gross_narion_production(self):
        narion = self.planet_narion_production + self.narion_plasmator * self.plasmator_production
        narion *= self.production_minister_bonus
        return int(narion)

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
        self.save()
        
    def pay_taxes(self):
        if self.alliance:
            self.alliance.pay_tax(self, self.metal_tax, self.crystal_tax, self.narion_tax)
        
    def exchange(self, input, output, amount):
        market = Market.objects.first()
        rate = {"metal":market.metal_rate, "crystal":market.crystal_rate, "narion":market.narion_rate}
        
        if input not in rate:
            raise ValueError("Input resource type does not exist!")
        if output not in rate:
            raise ValueError("Output resource type does not exist!")
        
        amount = min(amount, self.__dict__[input])
        amount = min(amount, market.__dict__[output] / rate[input])
        output_amount = min(amount * rate[input], market.__dict__[output])
                
        market.__dict__[input] += amount
        market.__dict__[output] -= output_amount
        market.save()

        self.__dict__[input] -= amount
        self.__dict__[output] += output_amount        
        self.save()
        
    def send_resources(self, receiver_planet, metal, crystal, narion):
        """Send resources to another planet in the same sol."""
        if self.sol != receiver_planet.sol:
            raise ValueError("Both planets must be in the same sol to send resources.")

        # Check if the sender has enough resources
        if metal > self.metal or crystal > self.crystal or narion > self.narion:
            raise ValueError("Not enough resources to send.")

        # Deduct resources from sender
        self.metal -= metal
        self.crystal -= crystal
        self.narion -= narion

        # Add resources to receiver
        receiver_planet.metal += metal
        receiver_planet.crystal += crystal
        receiver_planet.narion += narion

        # Save both planets
        self.save()
        receiver_planet.save()
