from django.db import models

from .round import Round

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
    metal = models.IntegerField(default=0)
    crystal = models.IntegerField(default=0)
    narion = models.IntegerField(default=0)

    def pay_tax(self, planet, metal, crystal, narion):
        self.metal += metal 
        self.crystal += crystal
        self.narion += narion

        turn = Round.objects.last().turn

        AllianceTreasuryLog.objects.create(
            alliance=self, 
            planet=planet, 
            turn=turn,
            metal=metal, 
            crystal=crystal, 
            narion=narion
        )
