from django.test import TestCase
from engine.models import Fleet, Ship, Planet

class FleetTestCase(TestCase):
    fixtures = ["planets", "fleets", "piraati_ships"]
    
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
        
        
    def test_swap_ship(self):
        """ Test swap_ship() method """
        pass
        
    def test_attack(self):
        """ Test attack() method """
        pass
        
    def test_defend(self):
        """ Test defend() method """
        pass
        
    def test_callback(self):
        """ Test callback() method """
        pass

    def test_tick(self):
        """ Test tick() method """
        pass
