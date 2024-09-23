from django.db import models

class PlanetRelocation(models.Model):
    planet = models.ForeignKey("Planet", on_delete=models.CASCADE, null=True, blank=True)
    turn = models.IntegerField(default=0)
    galaxy = models.ForeignKey("Galaxy", on_delete=models.CASCADE, default=None, null=True, blank=True)
    invitation = models.BooleanField(default=False, null=True, blank=True)
    outvote = models.BooleanField(default=False)

    def accept_invitation(self):
        if self.invitation:
            self.galaxy.add_planet(self.planet)
            self.delete_related_votes()
            PlanetRelocation.objects.filter(planet=self.planet).delete()
        else:
            raise ValueError("There is no active invitation")

    def delete_related_votes(self):
        from .galaxy import OutVote
        from .galaxy import CommanderVote
        OutVote.objects.filter(planet=self.planet).delete()
        OutVote.objects.filter(voter=self.planet).delete()
        CommanderVote.objects.filter(planet=self.planet).delete()
        CommanderVote.objects.filter(voter=self.planet).delete()

    def execute(self):
        from .round import Round

        round = Round.objects.order_by("number").last()
        if not self.invitation and round and self.turn <= round.turn:
            if self.outvote:
                if not self.galaxy.is_outvoted(self.planet):
                    self.delete_related_votes()
                    self.delete()
            if self.galaxy == None or self.outvote:
                from .galaxy import Galaxy
                galaxies = Galaxy.objects.all()
                not_full_galaxies = filter(lambda e:not e.full and e != self.galaxy, galaxies)
                not_full_galaxies = sorted(not_full_galaxies, key=lambda e: e.n_planets)
                if not_full_galaxies:
                    self.galaxy = not_full_galaxies[0]
                else:
                    for r in range(256):
                        for x in range(10):
                            for y in range(10):
                                try:
                                    Galaxy.objects.get(r=r, x=x, y=y)
                                except:
                                    self.galaxy = Galaxy.objects.create(r=r, x=x, y=y)
                                    self.galaxy.add_planet(self.planet)
                                    self.galaxy.save()
                                    self.delete()
                                    return None
            
            self.galaxy.add_planet(self.planet)
            self.galaxy.save()
            self.delete_related_votes()
            self.delete()
