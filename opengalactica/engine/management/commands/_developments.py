from engine.models import PlanetResearch

class Developments:
    def execute_planet_researches(self):
        for e in PlanetResearch.objects.filter(completed=False):
            e.start_research()
        
    def run(self):
        self.execute_planet_researches()
