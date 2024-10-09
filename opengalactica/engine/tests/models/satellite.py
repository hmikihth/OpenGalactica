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
        # Create a planet and satellite type
        self.planet = Planet.objects.create(name="Test Planet", metal=200, crystal=200, narion=200)
        self.satellite_type = SatelliteType.objects.create(
            name="Rocket", metal_cost=50, crystal_cost=50, narion_cost=50, production_time=5
        )

    def test_insufficient_resources(self):
        # Test when the planet doesn't have enough resources
        with self.assertRaises(ValueError):
            SatelliteProduction.objects.create(
                planet=self.planet,
                satellite_type=self.satellite_type,
                quantity=3  # Requires 150 metal, crystal, and narion
            )

    def test_sufficient_resources(self):
        # Test when the planet has enough resources
        production = SatelliteProduction.objects.create(
            planet=self.planet,
            satellite_type=self.satellite_type,
            quantity=2  # Requires 100 metal, crystal, and narion
        )

        self.planet.refresh_from_db()  # Reload planet data after production
        # Check if resources were deducted correctly
        self.assertEqual(self.planet.metal, 100)
        self.assertEqual(self.planet.crystal, 100)
        self.assertEqual(self.planet.narion, 100)

    def test_start_production(self):
        # Test starting satellite production and reducing turns
        production = SatelliteProduction.objects.create(
            planet=self.planet,
            satellite_type=self.satellite_type,
            quantity=1,
            turns_remaining=self.satellite_type.production_time,
            started=True
        )

        # Call start_production to reduce turns by 1
        production.start_production()

        # Reload production to check updated turns
        production.refresh_from_db()
        self.assertEqual(production.turns_remaining, 4)

    def test_complete_production(self):
        # Test the completion of satellite production
        production = SatelliteProduction.objects.create(
            planet=self.planet,
            satellite_type=self.satellite_type,
            quantity=2,
            turns_remaining=1,  # Set turns remaining to 1 to simulate production near completion
            started=True
        )

        # Call start_production to complete production
        production.start_production()

        # Check if the production is deleted after completion
        with self.assertRaises(SatelliteProduction.DoesNotExist):
            SatelliteProduction.objects.get(id=production.id)

        # Check if the quantity is correctly added to StockedSatellite
        stock = StockedSatellite.objects.get(planet=self.planet, satellite_type=self.satellite_type)
        self.assertEqual(stock.quantity, 2)
