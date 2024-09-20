from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .round import Round
from .planet import Planet

class AllianceTreasuryLog(models.Model):
    turn = models.IntegerField(default=0)
    alliance = models.ForeignKey("Alliance", on_delete=models.CASCADE, null=True, blank=True)
    planet = models.ForeignKey("Planet", on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=16)
    metal = models.IntegerField(default=0)
    crystal = models.IntegerField(default=0)
    narion = models.IntegerField(default=0)

class Alliance(models.Model):
    name = models.CharField(max_length=128)
    identifier = models.CharField(max_length=6)
    alliance_type = models.CharField(max_length=64, default="standard")
    metal = models.IntegerField(default=0)
    crystal = models.IntegerField(default=0)
    narion = models.IntegerField(default=0)
    credit = models.IntegerField(default=0)
    tax = models.IntegerField(
        default=20,         
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )
    
    def __str__(self):
        return f"#{self.identifier} - {self.name}"

    @property
    def members(self):
        return Planet.objects.filter(alliance=self)
        
    @property
    def n_members(self):
        return len(self.members)
        
    @property
    def tax_rate(self):
        return max(0, min(100, self.tax/100))

    @property
    def xp(self):
        return sum(map(lambda e:e.xp, self.members))

    @property
    def points(self):
        return sum(map(lambda e:e.points, self.members))


    def pay_tax(self, planet, metal, crystal, narion):
        if planet is None:
            raise ValueError("Only existing planets can pay tax")

        if planet.alliance != self:
            raise ValueError("Planet must be part of the alliance to pay tax")

        if metal < 0 or crystal < 0 or narion < 0:
            raise ValueError("Tax amounts must be positive")

        self.metal += metal 
        self.crystal += crystal
        self.narion += narion
        self.save()

        round = Round.objects.order_by("number").last()
        if round is None:
            raise ValueError("At least one round must exist")

        AllianceTreasuryLog.objects.create(
            alliance=self, 
            planet=planet, 
            turn=round.turn,
            type="tax",
            metal=metal, 
            crystal=crystal, 
            narion=narion
        )
