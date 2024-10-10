from django.test import TestCase
from engine.models import ShipModel, ShipProduction, Ship, ShipProto, Planet, Fleet

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


class ShipModelTestCase(TestCase):

    def setUp(self):
        # Create ShipModels with different properties
        self.fighter = ShipModel.objects.create(
            name="Fighter",
            ship_class="Fighter",
            metal=100,
            crystal=50,
            narion=30,
            hp=500,
            weapon_count=5,
            damage=20,
            evasion=10,
            accuracy_points=100,
            production_time=3
        )
        
        self.destroyer = ShipModel.objects.create(
            name="Destroyer",
            ship_class="Destroyer",
            metal=300,
            crystal=150,
            narion=90,
            hp=1000,
            weapon_count=10,
            damage=50,
            evasion=5,
            accuracy_points=120,
            production_time=5
        )
        
    def test_cost_calculation(self):
        # Test the cost calculation of a ship model
        fighter_proto = ShipProto()
        fighter_proto.ship_model = self.fighter

        self.assertEqual(fighter_proto.cost, 180)  # Fighter cost: 100 (metal) + 50 (crystal) + 30 (narion)

        destroyer_proto = ShipProto()
        destroyer_proto.ship_model = self.destroyer

        self.assertEqual(destroyer_proto.cost, 540)  # Destroyer cost: 300 (metal) + 150 (crystal) + 90 (narion)

    def test_target_order(self):
        # Test the target order property
        fighter_proto = ShipProto()
        fighter_proto.ship_model = self.fighter

        # Assuming fighter has default targets set as "-", should return the defaults
        self.assertEqual(fighter_proto.target_order, ("-", "-", "-"))

        # Test custom target assignment
        self.destroyer.target1 = "Fighter"
        self.destroyer.target2 = "Cruiser"
        self.destroyer.target3 = "Battleship"

        destroyer_proto = ShipProto()
        destroyer_proto.ship_model = self.destroyer
        self.assertEqual(destroyer_proto.target_order, ("Fighter", "Cruiser", "Battleship"))

    def test_hit_standard(self):
        # Test standard hit method
        fighter_proto = ShipProto()
        fighter_proto.ship_model = self.fighter
        fighter_proto.quantity = 10

        # Simulate an attack with damage and accuracy
        damage_taken = fighter_proto.hit_standard(damage=5000, accuracy=0.8)

        # Assert that the correct amount of ships is lost
        self.assertEqual(fighter_proto.loss, 0)  # No ships should be lost yet (hit_standard only calculates)
        self.assertEqual(fighter_proto.new_loss, 8)
        fighter_proto.apply_loss()  # Apply the loss
        self.assertEqual(fighter_proto.loss, 8)  # 8 out of 10 ships should be lost

    def test_hit_block(self):
        # Test blocker ship hit
        destroyer_proto = ShipProto()
        destroyer_proto.ship_model = self.destroyer
        destroyer_proto.quantity = 10

        # Simulate a blocker attack
        damage_blocked = destroyer_proto.hit_block(damage=10000, accuracy=0.9)

        # Assert that the blocker functionality reduces the number of combat-ready ships
        self.assertEqual(destroyer_proto.blocked, 0)
        self.assertEqual(destroyer_proto.new_blocked, 9)
        destroyer_proto.apply_block()  # Apply the block
        self.assertEqual(destroyer_proto.blocked, 9)  # 9 ships should be blocked from combat

    def test_hit_steal(self):
        # Test steal hit functionality
        fighter_proto = ShipProto()
        fighter_proto.ship_model = self.fighter
        fighter_proto.quantity = 10

        # Simulate a thief attack
        damage_stolen = fighter_proto.hit_steal(damage=4000)

        # Assert that the correct amount of ships is stolen
        self.assertEqual(fighter_proto.stolen, 0)
        self.assertEqual(fighter_proto.new_stolen, 2)  # Half of the damaged ships stolen
        fighter_proto.apply_steal()  # Apply the steal
        self.assertEqual(fighter_proto.stolen, 2)  # Confirm that 2 ships were stolen

    def test_fire_damage_calculation(self):
        # Test damage output when a ship fires
        destroyer_proto = ShipProto()
        destroyer_proto.ship_model = self.destroyer
        destroyer_proto.quantity = 10

        total_damage = destroyer_proto.fire()

        # The damage calculation should be based on quantity, weapon count, and damage value
        expected_damage = 10 * 10 * 50  # quantity * weapon_count * damage
        self.assertAlmostEqual(total_damage, expected_damage, delta=expected_damage * 0.02)

    def test_select_target(self):
        # Test target selection logic
        fighter_proto = ShipProto()
        destroyer_proto = ShipProto()

        fighter_proto.ship_model = self.fighter
        fighter_proto.quantity = 10
        destroyer_proto.ship_model = self.destroyer
        destroyer_proto.quantity = 5

        ships = [fighter_proto, destroyer_proto]

        # Test selecting all ships
        targets = fighter_proto.select_target("All", ships)
        self.assertEqual(len(targets), 2)  # Both the fighter and destroyer should be selected

        # Test selecting a specific target
        destroyer_targets = destroyer_proto.select_target("Destroyer", ships)
        self.assertEqual(len(destroyer_targets), 1)  # Only destroyers should be selected
        self.assertEqual(destroyer_targets[0].ship_model.name, "Destroyer")
