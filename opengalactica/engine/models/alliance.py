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

def set_new_founder_on_delete(collector, *args, **kwargs):
    planet = collector.origin
    alliance = planet.alliance
    planet.alliance = None
    planet.save()
    new_founder = alliance.set_new_founder()
    alliance.founder = new_founder 
    alliance.save()

class Alliance(models.Model):
    name = models.CharField(max_length=128)
    identifier = models.CharField(max_length=6)
    alliance_type = models.CharField(max_length=64, default="standard")
    founder = models.ForeignKey(
        "Planet", 
        related_name="founder", 
#        on_delete=lambda instance, *args, **kwargs: set_new_founder_on_delete(instance),
        on_delete=set_new_founder_on_delete,
        null=True, 
        blank=True
    )
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

    xp = models.IntegerField(default=0)
    xp_before = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    points_before = models.IntegerField(default=0)
    news = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        is_new = self._state.adding  # Check if the object is being created

        if is_new and not self.alliance_type:
            self.alliance_type = "standard"

        # Save the Alliance instance first
        super().save(*args, **kwargs)
        
        if is_new and self.founder:  # Check if it's a new instance and there's a founder
            self.set_new_founder(member=self.founder)

    def __str__(self):
        return f"#{self.identifier} - {self.name}"
    
    def set_new_founder(self, member=None):
        from .alliance_rank import AllianceRank
        forced_save = False

        if not member:
            def f(planet):
                if not planet.rank:
                    return (False, False, False, planet.points, planet.xp)
                return (planet.rank.can_set_ranks, planet.rank.can_invite_members, planet.rank != None, planet.points, planet.xp)

            ordered_members = sorted(self.members, key=f)

            if ordered_members:
                member = ordered_members[-1]
        else:
            forced_save = True
        if member:
            member.rank = self.founder_rank
            member.alliance = self
            member.save()
            if forced_save:
                self.founder = member
                self.save()
        return member
        
    @property
    def founder_rank(self):
        from .alliance_rank import AllianceRank
        return AllianceRank.objects.get(alliance_type=self.alliance_type, is_founder=True)

    @property
    def members(self):
        return Planet.objects.filter(alliance=self)
        
    @property
    def n_members(self):
        return len(self.members)
        
    @property
    def tax_rate(self):
        return max(0, min(100, self.tax/100))

    def recount_xp(self):
        self.xp_before = self.xp
        self.xp = sum(map(lambda e:e.xp, self.members))
        self.save()

    def recount_points(self):
        self.points_before = self.points
        self.points = sum(map(lambda e:e.points, self.members))
        self.save()

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
        
    def set_news(self, content):
        self.news = content
        self.save()

    @property
    def incoming_fleets(self):
        from .fleet import Fleet
        return Fleet.objects.filter(target__in=self.members, task="move")

    @property
    def outgoing_fleets(self):
        from .fleet import Fleet
        return Fleet.objects.filter(owner__in=self.members, task="move").exclude(target__isnull=True)
