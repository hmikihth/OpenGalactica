from django.db import models

class PlanetRelocation(models.Model):
    planet = models.ForeignKey("Planet", on_delete=models.CASCADE, null=True, blank=True)
    turn = models.IntegerField(default=0)
    sol = models.ForeignKey("Sol", on_delete=models.CASCADE, default=None, null=True, blank=True)
    invitation = models.BooleanField(default=False, null=True, blank=True)
    outvote = models.BooleanField(default=False)

    def accept_invitation(self):
        if self.invitation:
            self.sol.add_planet(self.planet)
            self.delete_related_votes()
            PlanetRelocation.objects.filter(planet=self.planet).delete()
        else:
            raise ValueError("There is no active invitation")

    def delete_related_votes(self):
        from .sol import OutVote
        from .sol import CommanderVote
        OutVote.objects.filter(planet=self.planet).delete()
        OutVote.objects.filter(voter=self.planet).delete()
        CommanderVote.objects.filter(planet=self.planet).delete()
        CommanderVote.objects.filter(voter=self.planet).delete()

    def execute(self):
        from .round import Round

        round = Round.objects.order_by("number").last()
        if not self.invitation and round and self.turn <= round.turn:
            if self.outvote:
                if not self.sol.is_outvoted(self.planet):
                    self.delete_related_votes()
                    self.delete()
            if self.sol == None or self.outvote:
                from .sol import Sol
                sols = Sol.objects.all()
                not_full_sols = filter(lambda e:not e.full and e != self.sol, sols)
                not_full_sols = sorted(not_full_sols, key=lambda e: e.n_planets)
                if not_full_sols:
                    self.sol = not_full_sols[0]
                else:
                    # The galaxies on 0:y:z coordinates are reserved for new planets
                    # The galaxies on 1:y:z are reserved for developers, admins and AI controlled planets
                    # Maximum ~9800 planets
                    for x in range(2,100):
                        for y in range(1,11):
                            try:
                                Sol.objects.get(x=x, y=y)
                            except:
                                self.sol = Sol.objects.create(x=x, y=y)
                                self.sol.add_planet(self.planet)
                                self.sol.save()
                                self.delete()
                                return None
            
            self.sol.add_planet(self.planet)
            self.sol.save()
            self.delete_related_votes()
            self.delete()
