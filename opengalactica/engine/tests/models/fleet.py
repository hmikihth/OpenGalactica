from django.test import TestCase
from engine.models import Fleet, Ship, Planet, Round

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
        """ Test swap_ship() method """
        pass

        # The method must remove ships from the fleet
        
        # The method must add the ships to the fleet
        
        # The method must not add ships to a moving fleet
        
        # The method must not remove ships from a moving fleet
        
        # The quantity must be a positive integer number
        
        # The quantity must be less or equal with the number of ships in the original fleet
        
        """Test swap_ship() method"""
        fleet1 = Fleet.objects.get(name="Empty Fleet 1")
        fleet2 = Fleet.objects.get(name="Empty Fleet 2")

        ship_model = Ship.objects.filter(fleet=fleet1).first().ship_model

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
        
        round = Round.objects.last()
        round.start_calculations()
        with self.assertRaises(ValueError, msg="Must fail when the turn calculations are running"):
            fleet1.swap_ship(fleet2, ship_model, 1)        
        round.end_calculations()

        
    def test_attack(self):
        """ Test attack() method """
        pass
        # Must fail when the turn calculations are running

        # The fleet must contain ships

        # The target must be unprotected
        
    def test_defend(self):
        """ Test defend() method """
        pass
        # Must fail when the turn calculations are running

        # The fleet must contain ships
        
    def test_callback(self):
        """ Test callback() method """
        pass
        # Must fail when the turn calculations are running

    def test_tick(self):
        """ Test tick() method """
        pass
