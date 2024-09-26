from django.test import TestCase
from engine.models import Planet, Round, PlanetRelocation

from engine.management.commands._moving_planets import MovingPlanets

class MovingPlanetsTestCase(TestCase):
    def setUp(self):
        self.round = Round.objects.create(number=1, turn=1)
        self.planet = Planet.objects.create(
            name="TestPlanet",
        )

    def test_start_sol_creates_relocation(self):
        MovingPlanets().run()
        relocations = PlanetRelocation.objects.filter(planet=self.planet)
        self.assertEqual(len(relocations), 1)
        
        # To make sure new running dont make more PlanetRelacations
        MovingPlanets().run()
        relocations = PlanetRelocation.objects.filter(planet=self.planet)
        self.assertEqual(len(relocations), 1)
        
    def test_planet_relocated_after_72_turns(self):
        MovingPlanets().run()

        old_coordinates = self.planet.coordinates

        self.round.turn += 72
        self.round.save()
        
        MovingPlanets().run()
        self.planet.refresh_from_db()
        
        new_coordinates = self.planet.coordinates
        
        self.assertNotEqual(old_coordinates, new_coordinates, "Planet should get new coordinates after 72 turns")