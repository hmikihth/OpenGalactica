from engine.models import Planet, Round, PlanetRelocation

class MovingPlanets:
    def run(self):
        turn = Round.objects.all().order_by("number").last().turn
        for planet in Planet.objects.all():
            planet.relocation(turn)
