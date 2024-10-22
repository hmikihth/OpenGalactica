from engine.models import Planet, Sol, Alliance

class PointCalculations:
    def run(self):
        for planet in Planet.objects.all():
            sol = planet.sol # DO NOT REMOVE! It creates the sol if doesnt exist yet
            planet.xp_before = planet.xp
            planet.save()
            planet.recount_points()

        for sol in Sol.objects.all():
            sol.recount_points()
            sol.recount_xp()

        for alliance in Alliance.objects.all():
            alliance.recount_points()
            alliance.recount_xp()
