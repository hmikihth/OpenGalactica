import random
from django.db import models

from .planet import Planet

class Galaxy(models.Model):
    name = models.CharField(max_length=128, default="-")
    commander = models.ForeignKey("Planet", related_name="commander", on_delete=models.SET_NULL, null=True, blank=True)
    minister_of_war = models.ForeignKey("Planet", related_name="minister_of_war", on_delete=models.SET_NULL, null=True, blank=True)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    @property
    def planets(self):
        return Planet.objects.filter(x=self.x, y=self.y).order_by("z")
        
    @property
    def n_planets(self):
        return len(self.planets)
        
    @property
    def n_relocations(self):
        from .planet_relocation import PlanetRelocation
        return len(PlanetRelocation.objects.filter(galaxy=self))

    @property
    def full(self):
        return self.n_planets + self.n_relocations > 9        
            
    @property
    def current_outvotes(self):
        from .planet_relocation import PlanetRelocation
        return PlanetRelocation.objects.filter(galaxy=self, outvote=True)

    @property
    def xp(self):
        return sum(map(lambda e:e.xp, self.planets))
            
    @property
    def points(self):
        return sum(map(lambda e:e.points, self.planets))

    def add_planet(self, planet):
        if not self.full:
            busy = Planet.objects.filter(x=self.x, y=self.y).values_list("z", flat=True)
            z = random.choice([*filter(lambda e: e not in busy, range(1,11))])
            planet.x = self.x
            planet.y = self.y
            planet.z = z
            planet.save()
        else:
            raise ValueError("The galaxy is full")

    def invite(self, planet):
        if self.full:
            raise ValueError("The galaxy is full")
        else:
            from .planet_relocation import PlanetRelocation
            PlanetRelocation.objects.create(planet=planet, galaxy=self, invitation=True)
        
    def start_outvote(self, planet):
        from .planet import PlanetRelocation
        from .round import Round
        round = Round.objects.sorted("number").last()
        PlanetRelocation.objects.create(planet=planet, galaxy=self, turn=round.turn+72, outvote=True)

    def cancel_outvote(self, planet):
        from .planet_relocation import PlanetRelocation
        PlanetRelocation.objects.filter(planet=planet, galaxy=self, outvote=True).delete()
        OutVote.objects.filter(planet=planet).delete()

    def send_vote_outvote(self, planet, voter, value):
        if planet.galaxy != voter.galaxy or voter.galaxy != self:
            raise ValueError("The the target planet and the voter have to be in the galaxy")
        obj, created = OutVote.objects.get_or_create(planet=planet, voter=voter, galaxy=self)
        obj.value = value
        obj.save()

    def is_outvoted(self, planet):
        return len(OutVote.objects.filter(value=True)) > (self.n_planets-1)//2
        
    def set_commander(self):
        commander = None
        votes = CommanderVote.objects.filter(galaxy=self).exclude(planet=None)
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
        if planet.galaxy != voter.galaxy or voter.galaxy != self:
            raise ValueError("The the target planet and the voter have to be in the galaxy")
        obj, created = CommanderVote.objects.get_or_create(voter=voter, galaxy=self)
        obj.planet = planet
        obj.save()
        self.set_commander()

        
class CommanderVote(models.Model):
    galaxy = models.ForeignKey("Galaxy", on_delete=models.CASCADE, default=None, null=True, blank=True)
    planet = models.ForeignKey("Planet", related_name="commander_votes", on_delete=models.CASCADE, null=True, blank=True)
    voter = models.ForeignKey("Planet", related_name="voted_for_commander", on_delete=models.CASCADE, null=True, blank=True)


class OutVote(models.Model):
    galaxy = models.ForeignKey("Galaxy", on_delete=models.CASCADE, default=None, null=True, blank=True)
    planet = models.ForeignKey("Planet", related_name="outvotes", on_delete=models.CASCADE, null=True, blank=True)
    voter = models.ForeignKey("Planet", related_name="voted_for_outvotes", on_delete=models.CASCADE, null=True, blank=True)
    value = models.BooleanField(default=None, null=True, blank=True)
