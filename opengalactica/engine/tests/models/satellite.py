from django.test import TestCase
from engine.models import SatelliteType, StockedSatellite, SatelliteProduction, Planet

class SatelliteTypeTestCase(TestCase):
    def setUp(self):
        self.satellite_type = SatelliteType.objects.create(
            name="Rocket", 
            description="Basic rocket used for activating other probes.", 
            metal=100, 
            crystal=50, 
            narion=30, 
            production_time=2, 
            requires_rocket=False,
            rocket_required_count=0
        )

    def test_satellite_type_creation(self):
        self.assertEqual(self.satellite_type.name, "Rocket")
        self.assertEqual(self.satellite_type.metal, 100)
        self.assertEqual(self.satellite_type.crystal, 50)
        self.assertEqual(self.satellite_type.narion, 30)
        self.assertEqual(self.satellite_type.production_time, 2)
        self.assertFalse(self.satellite_type.requires_rocket)
        self.assertEqual(self.satellite_type.rocket_required_count, 0)

class StockedSatelliteTestCase(TestCase):
    def setUp(self):
        self.planet = Planet.objects.create(name="Earth")
        self.satellite_type = SatelliteType.objects.create(
            name="Planet Probe", 
            description="Used to gather planet information.",
            metal=200, 
            crystal=150, 
            narion=100, 
            production_time=3, 
            requires_rocket=True,
            rocket_required_count=2
        )
        self.stocked_satellite = StockedSatellite.objects.create(
            planet=self.planet, 
            satellite_type=self.satellite_type, 
            quantity=5
        )

    def test_stocked_satellite_creation(self):
        self.assertEqual(self.stocked_satellite.planet, self.planet)
        self.assertEqual(self.stocked_satellite.satellite_type, self.satellite_type)
        self.assertEqual(self.stocked_satellite.quantity, 5)

    def test_stocked_satellite_costs(self):
        self.assertEqual(self.stocked_satellite.metal, 200)
        self.assertEqual(self.stocked_satellite.crystal, 150)
        self.assertEqual(self.stocked_satellite.narion, 100)
        self.assertEqual(self.stocked_satellite.points, 450)

class SatelliteProductionTestCase(TestCase):
    def setUp(self):
        self.planet = Planet.objects.create(name="Mars")
        self.satellite_type = SatelliteType.objects.create(
            name="Interceptor Probe", 
            description="Destroys enemy probes trying to gather information.",
            metal=300, 
            crystal=200, 
            narion=150, 
            production_time=5, 
            requires_rocket=False,
            rocket_required_count=0
        )
        self.production = SatelliteProduction.objects.create(
            planet=self.planet, 
            satellite_type=self.satellite_type, 
            quantity=2, 
            turns_remaining=None, 
        )

    def test_satellite_production_creation(self):
        self.assertEqual(self.production.planet, self.planet)
        self.assertEqual(self.production.satellite_type, self.satellite_type)
        self.assertEqual(self.production.quantity, 2)
        self.assertEqual(self.production.turns_remaining, 5)  # Defaults to production time

    def test_start_production(self):
        self.production.start_production()
        self.assertEqual(self.production.turns_remaining, 4)
        self.production.start_production()
        self.assertEqual(self.production.turns_remaining, 3)

    def test_complete_production(self):
        for _ in range(5):
            self.production.start_production()

        # Check that the production is deleted and satellites are stocked
        self.assertFalse(SatelliteProduction.objects.filter(id=self.production.id).exists())
        stock = StockedSatellite.objects.get(planet=self.planet, satellite_type=self.satellite_type)
        self.assertEqual(stock.quantity, 2)
