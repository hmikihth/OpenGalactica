import random
from django.db import models

from .planet import Planet

class Sol(models.Model):
    name = models.CharField(max_length=128, default="-")
    commander = models.ForeignKey("Planet", related_name="commander", on_delete=models.SET_NULL, null=True, blank=True)
    minister_of_war = models.ForeignKey("Planet", related_name="minister_of_war", on_delete=models.SET_NULL, null=True, blank=True)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    xp_before = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    points_before = models.IntegerField(default=0)
    ministers_message = models.TextField(blank=True, null=True)

    @property
    def planets(self):
        return Planet.objects.filter(x=self.x, y=self.y).order_by("z")
        
    @property
    def n_planets(self):
        return len(self.planets)
        
    @property
    def n_relocations(self):
        from .planet_relocation import PlanetRelocation
        return len(PlanetRelocation.objects.filter(sol=self))

    @property
    def full(self):
        return self.n_planets + self.n_relocations > 9        
            
    @property
    def current_outvotes(self):
        from .planet_relocation import PlanetRelocation
        return PlanetRelocation.objects.filter(sol=self, outvote=True)

    def recount_xp(self):
        self.xp_before = self.xp
        self.xp = sum(map(lambda e:e.xp, self.planets))
        self.save()
            
    def recount_points(self):
        self.points_before = self.points
        self.points = sum(map(lambda e:e.points, self.planets))
        self.save()

    def add_planet(self, planet):
        if not self.full:
            busy = Planet.objects.filter(x=self.x, y=self.y).values_list("z", flat=True)
            z = random.choice([*filter(lambda e: e not in busy, range(1,11))])
            planet.x = self.x
            planet.y = self.y
            planet.z = z
            planet.save()
        else:
            raise ValueError("The sol is full")

    def invite(self, planet):
        if self.full:
            raise ValueError("The sol is full")
        else:
            from .planet_relocation import PlanetRelocation
            PlanetRelocation.objects.create(planet=planet, sol=self, invitation=True)
        
    def start_outvote(self, planet):
        from .planet import PlanetRelocation
        from .round import Round
        round = Round.objects.sorted("number").last()
        PlanetRelocation.objects.create(planet=planet, sol=self, turn=round.turn+72, outvote=True)

    def cancel_outvote(self, planet):
        from .planet_relocation import PlanetRelocation
        PlanetRelocation.objects.filter(planet=planet, sol=self, outvote=True).delete()
        OutVote.objects.filter(planet=planet).delete()

    def send_vote_outvote(self, planet, voter, value):
        if planet.sol != voter.sol or voter.sol != self:
            raise ValueError("The the target planet and the voter have to be in the sol")
        obj, created = OutVote.objects.get_or_create(planet=planet, voter=voter, sol=self)
        obj.value = value
        obj.save()

    def is_outvoted(self, planet):
        return len(OutVote.objects.filter(value=True)) > (self.n_planets-1)//2
        
    def set_commander(self):
        commander = None
        votes = CommanderVote.objects.filter(sol=self).exclude(planet=None)
        if len(votes):
            vl = votes.values_list("planet", flat=True)
            planets = {*Planet.objects.filter(id__in=vl)}
            planet_votes = {e:len(votes.filter(planet=e)) for e in planets}
            sorted_votes = sorted(planets, key=lambda e:-planet_votes[e])
            if len(sorted_votes) == 1 or planet_votes[sorted_votes[0]] != planet_votes[sorted_votes[1]]:
                commander = sorted_votes[0]
        self.commander = commander
        self.save()
            
        
    def send_vote_commander(self, planet, voter):
        if planet.sol != voter.sol or voter.sol != self:
            raise ValueError("The the target planet and the voter have to be in the sol")
        obj, created = CommanderVote.objects.get_or_create(voter=voter, sol=self)
        obj.planet = planet
        obj.save()
        self.set_commander()
        
    @property
    def ministers_message_content(self):
        return self.ministers_message

    def set_ministers_message(self, planet, message):
        if planet != self.commander and planet != self.minister_of_war:
            raise PermissionError("You don't have permission to update the ministers' message.")
        self.ministers_message = message
        self.save()
    
    @property
    def incoming_fleets(self):
        from .fleet import Fleet
        return Fleet.objects.filter(target__in=self.planets)

    @property
    def outgoing_fleets(self):
        from .fleet import Fleet
        return Fleet.objects.filter(owner__in=self.planets).exclude(target__isnull=True)

        
class CommanderVote(models.Model):
    sol = models.ForeignKey("Sol", on_delete=models.CASCADE, default=None, null=True, blank=True)
    planet = models.ForeignKey("Planet", related_name="commander_votes", on_delete=models.CASCADE, null=True, blank=True)
    voter = models.ForeignKey("Planet", related_name="voted_for_commander", on_delete=models.CASCADE, null=True, blank=True)


class OutVote(models.Model):
    sol = models.ForeignKey("Sol", on_delete=models.CASCADE, default=None, null=True, blank=True)
    planet = models.ForeignKey("Planet", related_name="outvotes", on_delete=models.CASCADE, null=True, blank=True)
    voter = models.ForeignKey("Planet", related_name="voted_for_outvotes", on_delete=models.CASCADE, null=True, blank=True)
    value = models.BooleanField(default=None, null=True, blank=True)
