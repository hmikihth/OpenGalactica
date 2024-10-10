from django.test import TestCase
from engine.models import ShipModel, ShipProduction, Ship, Planet, Fleet

class ShipProductionTestCase(TestCase):

    def setUp(self):
        # Create a planet with some resources
        self.planet = Planet.objects.create(name="Test Planet", metal=500, crystal=500, narion=500)

        # Create a ShipModel with specific resource costs
        self.ship_model = ShipModel.objects.create(
            name="Fighter",
            metal=100,
            crystal=100,
            narion=100,
            production_time=3
        )

    def test_insufficient_resources(self):
        # Try to create a ShipProduction with not enough resources
        with self.assertRaises(ValueError):
            ShipProduction.objects.create(
                planet=self.planet,
                ship_model=self.ship_model,
                quantity=6  # Requires 600 metal, 600 crystal, 600 narion, which exceeds planet's resources
            )

    def test_sufficient_resources(self):
        # Create ShipProduction with enough resources
        production = ShipProduction.objects.create(
            planet=self.planet,
            ship_model=self.ship_model,
            quantity=3  # Requires 300 metal, 300 crystal, 300 narion, which is within planet's resources
        )

        self.planet.refresh_from_db()

        # Check if planet's resources are correctly deducted
        self.assertEqual(self.planet.metal, 200)
        self.assertEqual(self.planet.crystal, 200)
        self.assertEqual(self.planet.narion, 200)

    def test_start_production(self):
        # Create a ShipProduction and simulate production progress
        production = ShipProduction.objects.create(
            planet=self.planet,
            ship_model=self.ship_model,
            quantity=2,
            turns_remaining=self.ship_model.production_time  # Start with full production time
        )

        # Start production, should reduce turns remaining
        production.start_production()
        production.refresh_from_db()

        self.assertEqual(production.turns_remaining, 2)  # Turns remaining should reduce by 1

    def test_complete_production(self):
        # Create ShipProduction near completion (1 turn remaining)
        production = ShipProduction.objects.create(
            planet=self.planet,
            ship_model=self.ship_model,
            quantity=3,
            turns_remaining=1  # 1 turn left to complete production
        )

        # Get or create a base for the planet
        fleet, _ = Fleet.objects.get_or_create(owner=self.planet, base=True)

        # Simulate production completion
        result = production.start_production()

        # Check if production is completed (object deleted)
        with self.assertRaises(ShipProduction.DoesNotExist):
            ShipProduction.objects.get(id=production.id)

        # Check if the ships were added to the fleet
        stock = Ship.objects.get(fleet=fleet, ship_model=self.ship_model)
        self.assertEqual(stock.quantity, 3)  # Ships should be added to the fleet

        self.assertTrue(result)  # Production should return True when completed

    def test_production_does_not_continue_past_completion(self):
        # Create ShipProduction with 1 turn remaining, then complete it
        production = ShipProduction.objects.create(
            planet=self.planet,
            ship_model=self.ship_model,
            quantity=1,
            turns_remaining=1
        )

        # Complete the production
        production.start_production()

        # Call start_production again, should not raise an error and should not alter the state
        production.start_production()
        # No additional actions should occur as the production was already completed and deleted
