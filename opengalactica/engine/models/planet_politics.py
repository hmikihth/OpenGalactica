from .planet_relocation import PlanetRelocation

class PlanetPolitics:
    @property
    def galaxy(self):
        from .galaxy import Galaxy
        galaxy, created = Galaxy.objects.get_or_create(x=self.x, y=self.y)
        return galaxy
    
    @property
    def is_minister(self):
        return self in (self.galaxy.commander, self.galaxy.minister_of_war)
                                
    def relocation(self, turn):
        rl = None
        try:
            rl = PlanetRelocation.objects.filter(planet=self, turn__lte=turn).last()
        except:
            pass
        if rl:
            rl.execute()
