from django.test import TestCase
from engine.models import Fleet, Ship, ShipModel, Planet, Round

class FleetTestCase(TestCase):
    fixtures = ["planets", "fleets", "piraati_ships", "round"]
    
    def test_add_ship(self):
        """Test add_ship() method"""
        fleet = Fleet.objects.get(name="Fleet 1")

        ships = Ship.objects.filter(fleet=fleet).first()
        original = ships.quantity

        fleet.add_ship(ships.ship_model, 10)

        ships.refresh_from_db()
        new = ships.quantity
        
        self.assertEqual(original+10, new,
            """The quantity should increase"""
        )
        
        with self.assertRaises(ValueError):
            fleet.add_ship(ships.ship_model, -1)

        round = Round.objects.last()
        round.start_calculations()
        with self.assertRaises(ValueError, msg="Must fail when the turn calculations are running"):
            fleet.add_ship(ships.ship_model, 3)
        round.end_calculations()
        
        
    def test_swap_ship(self):
        """Test swap_ship() method"""
        fleet1 = Fleet.objects.get(name="Empty Fleet 1")
        fleet2 = Fleet.objects.get(name="Empty Fleet 2")
        

        # To make sure fleet is empty and standing
        fleet1.task = "stand"
        fleet1.save()
        Ship.objects.filter(fleet=fleet1).delete()

        ship_model = ShipModel.objects.first()

        # Add ships to both fleets
        fleet1.add_ship(ship_model, 10)
        fleet2.add_ship(ship_model, 5)

        # Validate swap with valid quantity
        fleet1.swap_ship(fleet2, ship_model, 5)

        fleet1_ship = Ship.objects.filter(fleet=fleet1, ship_model=ship_model).first()
        fleet2_ship = Ship.objects.filter(fleet=fleet2, ship_model=ship_model).first()

        self.assertEqual(fleet1_ship.quantity, 5, "Fleet 1 should have 5 ships left after swap")
        self.assertEqual(fleet2_ship.quantity, 10, "Fleet 2 should have 10 ships after swap")

        # Validate swapping more than available ships
        with self.assertRaises(ValueError, msg="Should raise ValueError when swapping more ships than available"):
            fleet1.swap_ship(fleet2, ship_model, 6)

        # Validate swapping with zero or negative quantity
        with self.assertRaises(ValueError, msg="Should raise ValueError when swapping with zero quantity"):
            fleet1.swap_ship(fleet2, ship_model, 0)

        with self.assertRaises(ValueError, msg="Should raise ValueError when swapping with negative quantity"):
            fleet1.swap_ship(fleet2, ship_model, -5)

        # Start calculation to validate that swap is prevented if turn calculation is running
        round = Round.objects.last()
        round.start_calculations()

        with self.assertRaises(ValueError, msg="Must fail when the turn calculations are running"):
            fleet1.swap_ship(fleet2, ship_model, 1)        

        round.end_calculations()

        # Set fleet1 to move and validate that the swap is prevented
        fleet1.task = "move"
        fleet1.save()

        with self.assertRaises(ValueError, msg="Should raise ValueError when swapping from a moving fleet"):
            fleet1.swap_ship(fleet2, ship_model, 1)

        # Set fleet2 to move and validate that the swap is prevented
        fleet2.task = "move"
        fleet2.save()

        with self.assertRaises(ValueError, msg="Should raise ValueError when swapping to a moving fleet"):
            fleet1.swap_ship(fleet2, ship_model, 1)        
        
        
    def test_attack(self):
        fleet = Fleet.objects.get(name="Fleet 1")
        target_planet = Planet.objects.get(name="Test Planet 1")
        
        # Ensure attack fails when no ships
        Ship.objects.filter(fleet=fleet).delete()
        with self.assertRaises(ValueError, msg="Fleet has no ships"):
            fleet.attack(2, target_planet)

        # Add ships and ensure attack succeeds
        ship_model = Ship.objects.first().ship_model
        fleet.add_ship(ship_model, 10)
        
        # Start calculation to prevent attack
        round = Round.objects.last()
        round.start_calculations()
        
        with self.assertRaises(ValueError, msg="Turn calculation is running"):
            fleet.attack(2, target_planet)
        
        round.end_calculations()

        # Set the distance to 0 to check the method will set a new value
        fleet.distance = 0
        fleet.save()

        # Verify attack
        fleet.attack(2, target_planet)
        self.assertEqual(fleet.task, "attack")
        self.assertEqual(fleet.target, target_planet)
        self.assertEqual(fleet.distance, target_planet.get_distance(fleet), "Must set the distance")
        
        # Must fail if they fleet's owner planet and the target are in the same galaxy or in the same alliance

    def test_defend(self):
        fleet = Fleet.objects.get(name="Fleet 1")
        target_planet = Planet.objects.get(name="Test Planet 1")
        
        # Ensure defense fails when no ships
        Ship.objects.filter(fleet=fleet).delete()
        with self.assertRaises(ValueError, msg="Fleet has no ships"):
            fleet.defend(2, target_planet)

        # Add ships and ensure defend succeeds
        ship_model = Ship.objects.first().ship_model
        fleet.add_ship(ship_model, 10)
        
        # Start calculation to prevent defend
        round = Round.objects.last()
        round.start_calculations()
        
        with self.assertRaises(ValueError, msg="Turn calculation is running"):
            fleet.defend(2, target_planet)
        
        round.end_calculations()

        # Set the distance to 0 to check the method will set a new value
        fleet.distance = 0
        fleet.save()

        # Verify defend
        fleet.defend(2, target_planet)
        self.assertEqual(fleet.task, "defend")
        self.assertEqual(fleet.target, target_planet)
        self.assertEqual(fleet.distance, target_planet.get_distance(fleet), "Must set the distance")

    def test_callback(self):
        fleet = Fleet.objects.get(name="Fleet 1")
        
        # Ensure callback fails when fleet is already at home
        fleet.task = "stand"
        fleet.target = None
        fleet.save()

        with self.assertRaises(ValueError, msg="Must fail if the fleet is already at home"):
            fleet.callback()
        
        # Simulate fleet moving and callback to return home
        fleet.task = "move"
        target_planet = Planet.objects.get(name="Test Planet 1")
        fleet.target = target_planet
        fleet.distance = target_planet.get_distance(fleet)
        fleet.save()

        old_distance = fleet.distance
        fleet.distance -= 1
        fleet.save()

        fleet.callback()
        fleet.refresh_from_db()

        self.assertEqual(fleet.task, "return", "Fleet should be in return mode after callback")
        self.assertEqual(fleet.target, target_planet, "Fleet should keep the target after callback")
        self.assertEqual(fleet.distance, 1, "Must recount the distance")
        
    def test_tick(self):
        """ Test tick() method """

        fleet = Fleet.objects.get(name="Fleet 1")
  
        # Test error when calculations are not running
        round = Round.objects.last()
        round.end_calculations()
        
        with self.assertRaises(ValueError, msg="Turn calculation is not running"):
            fleet.tick()
        
        round.start_calculations()
        
        # Test error for base fleet
        fleet.base = True
        fleet.save()
        
        with self.assertRaises(ValueError, msg="Base fleets cannot move"):
            fleet.tick()
        
        fleet.base = False
        fleet.save()
        
        # Test distance decrement
        fleet.distance = 3
        fleet.tick()
        self.assertEqual(fleet.distance, 2, "Distance should decrease by 1")
        
        # Test turn decrement when distance reaches zero
        fleet.distance = 1
        fleet.task = "move"
        fleet.tick()
        fleet.refresh_from_db()
        self.assertEqual(fleet.distance, 0, "Distance should be zero")


        fleet.distance = 0
        fleet.task = "move"
        fleet.turns = 2
        fleet.tick()
        fleet.refresh_from_db()
        self.assertEqual(fleet.turns, 1, "Turns should decrease by 1")
        
        fleet.tick()
        fleet.refresh_from_db()
        self.assertEqual(fleet.task, "return", "Fleet should switch to return mode")
        
        # Test returning home
        fleet.distance = 1
        fleet.task = "return"
        fleet.tick()
        fleet.refresh_from_db()
        self.assertEqual(fleet.distance, 0, "Fleet should be home")
        self.assertEqual(fleet.task, "stand", "Task should be set to stand")
        self.assertIsNone(fleet.target, "Target should be reset")
        self.assertEqual(fleet.role, "Defenders", "Role should be set to Defenders")
        
        # Test instant return home if no ships remain
        Ship.objects.filter(fleet=fleet).delete()
        fleet.task = "move"
        fleet.distance = 2
        fleet.tick()
        fleet.refresh_from_db()
        self.assertEqual(fleet.distance, 0, "Fleet should return home instantly if no ships remain")
        self.assertEqual(fleet.task, "stand", "Task should be set to stand")
        self.assertIsNone(fleet.target, "Target should be reset")
