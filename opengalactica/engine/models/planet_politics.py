from .planet_relocation import PlanetRelocation

class PlanetPolitics:
    @property
    def sol(self):
        from .sol import Sol
        sol, created = Sol.objects.get_or_create(x=self.x, y=self.y)
        return sol
    
    @property
    def is_minister(self):
        return self in (self.sol.commander, self.sol.minister_of_war)
                                
    def relocation(self, turn):
        rl = None
        try:
            rl = PlanetRelocation.objects.filter(planet=self, turn__lte=turn).last()
        except:
            pass
        if rl:
            rl.execute()
