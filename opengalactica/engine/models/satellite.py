from django.db import models

class SatelliteType(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    metal = models.IntegerField()
    crystal = models.IntegerField()
    narion = models.IntegerField()
    production_time = models.IntegerField()  # in turns
    requires_rocket = models.BooleanField(default=True)  # Indicates if rockets are needed for activation
    rocket_required_count = models.IntegerField(default=0)  # Number of rockets required, 0 if not applicable
    requirement = models.ForeignKey('Research', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

    @property
    def points(self):
        return sum((self.metal, self.crystal, self.narion)) * 0.01


class StockedSatellite(models.Model):
    planet = models.ForeignKey("Planet", on_delete=models.CASCADE)
    satellite_type = models.ForeignKey(SatelliteType, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    @property
    def metal(self):
        return self.satellite_type.metal
        
    @property
    def crystal(self):
        return self.satellite_type.crystal
        
    @property
    def narion(self):
        return self.satellite_type.narion

    @property
    def points(self):
        return self.satellite_type.points * self.quantity


class SatelliteProduction(models.Model):
    planet = models.ForeignKey("Planet", on_delete=models.CASCADE)
    satellite_type = models.ForeignKey(SatelliteType, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    turns_remaining = models.IntegerField()  # Production time remaining

    def save(self, *args, **kwargs):
        total_metal_cost = self.satellite_type.metal * self.quantity
        total_crystal_cost = self.satellite_type.crystal * self.quantity
        total_narion_cost = self.satellite_type.narion * self.quantity

        # Check if the planet has enough resources
        if (self.planet.metal < total_metal_cost or 
            self.planet.crystal < total_crystal_cost or 
            self.planet.narion < total_narion_cost):
            raise ValueError("Not enough resources to produce the satellites.")
        else:
            # Deduct the resources from the planet
            self.planet.metal -= total_metal_cost
            self.planet.crystal -= total_crystal_cost
            self.planet.narion -= total_narion_cost
            self.planet.save()  # Save the planet after deducting resources

        if self.turns_remaining is None:
            self.turns_remaining = self.satellite_type.production_time
        return super().save(*args, **kwargs)

    def start_production(self):
        """Start or continue satellite production."""
        if self.turns_remaining > 0:
            self.turns_remaining -= 1
            if self.turns_remaining <= 0:
                stock, _ = StockedSatellite.objects.get_or_create(planet=self.planet, satellite_type=self.satellite_type)
                stock.quantity += self.quantity
                stock.save()
                self.delete()
                return True
            self.save()

    def __str__(self):
        return f"{self.planet} - {self.satellite_type.name} (Turns left: {self.turns_remaining})"