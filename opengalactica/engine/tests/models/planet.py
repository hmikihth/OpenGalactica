from django.test import TestCase
from engine.models import Planet

class PlanetTestCase(TestCase):
    def setUp(self):
        Planet.objects.create(
            name = "TestPlanet",
            r = 0,
            x = 1,
            y = 2,
            z = 3,
        )
        
    def test_coordinates(self):
        """Test coordinates property"""
        planet = Planet.objects.first()
        self.assertEqual(planet.coordinates, "0:1:2:3")

    def test_coordinates(self):
        """Test __str__ method"""
        planet = Planet.objects.first()
        self.assertEqual(str(planet), "TestPlanet (0:1:2:3)")
