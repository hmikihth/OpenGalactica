from django.test import TestCase
from engine.models import Planet, Fleet, Alliance, Market, MAX_FLEETS

class PlanetTestCase(TestCase):
    def setUp(self):
        self.planet = Planet.objects.create(
            name="TestPlanet",
            r=0,
            x=1,
            y=2,
            z=3,
        )
        
    def test_coordinates(self):
        """Test coordinates property"""
        self.assertEqual(self.planet.coordinates, "0:1:2:3")

    def test_str_method(self):
        """Test __str__ method"""
        self.assertEqual(str(self.planet), "TestPlanet (0:1:2:3)")

    def test_fleet_creation_on_save(self):
        """Test that the save() method creates the base fleet and additional fleets"""
        
        # Ensure planet is saved properly
        self.planet.save()
        
        # Check that the base fleet and other fleets were created
        fleets = Fleet.objects.filter(owner=self.planet, base=False)
        self.assertEqual(fleets.count(), MAX_FLEETS, "The correct number of fleets should be created")
        
        # Check that the first fleet is the base fleet
        base_fleet = Fleet.objects.filter(owner=self.planet, base=True).first()
        self.assertIsNotNone(base_fleet, "There should be a base fleet created")
        self.assertEqual(base_fleet.name, "Base", "The base fleet should be named 'Base'")
        
        # Check that other fleets are named correctly
        for i, fleet in enumerate(fleets):
            if not fleet.base:
                self.assertEqual(fleet.name, f"Fleet {i+1}", f"Fleet {i+1} should be named 'Fleet {i+1}'")

    def test_default_field_values(self):
        """Test that the default field values are set correctly"""
        self.assertEqual(self.planet.metal, 0, "Default metal value should be 0")
        self.assertEqual(self.planet.crystal, 0, "Default crystal value should be 0")
        self.assertEqual(self.planet.narion, 0, "Default narion value should be 0")
        self.assertEqual(self.planet.credit, 0, "Default credit value should be 0")
        self.assertEqual(self.planet.protection, 72, "Default protection value should be 72")
        self.assertFalse(self.planet.on_holiday, "Default value for on_holiday should be False")
        
        
class PlanetEconomyTestCase(TestCase):
    fixtures = ["round"]
    def setUp(self):
        """Set up a planet and alliance for testing."""
        # Create Alliance for tests
        self.alliance = Alliance.objects.create(name="Test Alliance", identifier="TA123", tax=20)
        self.planet = Planet.objects.create(
            name="EconomyPlanet",
            metal_plasmator=50,
            crystal_plasmator=50,
            narion_plasmator=50,
            neutral_plasmator=0,
            alliance=self.alliance
        )

        Market.objects.all().delete()
        self.market = Market.objects.create()

    def test_active_plasmators(self):
        """Test active_plasmators property."""
        self.assertEqual(self.planet.active_plasmators, 150)

    def test_plasmators(self):
        """Test plasmators property."""
        self.planet.neutral_plasmator = 10
        self.assertEqual(self.planet.plasmators, 160)

    def test_plasmator_production_below_100(self):
        """Test plasmator_production when active_plasmators < 100."""
        self.planet.metal_plasmator = 90
        self.planet.crystal_plasmator = 0
        self.planet.narion_plasmator = 0
        self.assertEqual(self.planet.plasmator_production, 500)

    def test_plasmator_production_above_1000(self):
        """Test plasmator_production when active_plasmators > 1000."""
        self.planet.metal_plasmator = 1001
        self.planet.crystal_plasmator = 0
        self.planet.narion_plasmator = 0
        self.assertEqual(self.planet.plasmator_production, 400)

    def test_plasmator_production_between_100_and_1000(self):
        """Test plasmator_production when active_plasmators are between 100 and 1000."""
        self.planet.metal_plasmator = 500
        self.planet.crystal_plasmator = 0
        self.planet.narion_plasmator = 0
        expected_value = 510 - (11 * 500) // 100  # 455
        self.assertEqual(self.planet.plasmator_production, expected_value)

    def test_gross_productions(self):
        """Test gross metal, crystal, and narion production."""
        self.planet.metal_plasmator = 100
        self.planet.crystal_plasmator = 100
        self.planet.narion_plasmator = 100
        production = self.planet.plasmator_production

        # Assuming no minister bonus
        expected_metal = 1000 + 100 * production
        expected_crystal = 1000 + 100 * production
        expected_narion = 1000 + 100 * production

        self.assertEqual(self.planet.gross_metal_production, expected_metal)
        self.assertEqual(self.planet.gross_crystal_production, expected_crystal)
        self.assertEqual(self.planet.gross_narion_production, expected_narion)

    def test_taxes(self):
        """Test the tax calculations for metal, crystal, and narion."""
        tax = 20
        tax_rate = tax/100
        self.planet.metal_plasmator = 100
        self.planet.crystal_plasmator = 100
        self.planet.narion_plasmator = 100
        self.planet.alliance.tax = tax

        
        gross_metal = self.planet.gross_metal_production
        gross_crystal = self.planet.gross_crystal_production
        gross_narion = self.planet.gross_narion_production

        self.assertEqual(self.planet.metal_tax, int(gross_metal * tax_rate))
        self.assertEqual(self.planet.crystal_tax, int(gross_crystal * tax_rate))
        self.assertEqual(self.planet.narion_tax, int(gross_narion * tax_rate))

    def test_net_productions(self):
        """Test net metal, crystal, and narion production after taxes."""
        gross_metal = self.planet.gross_metal_production
        gross_crystal = self.planet.gross_crystal_production
        gross_narion = self.planet.gross_narion_production
        tax_rate = self.planet.alliance.tax_rate

        net_metal = gross_metal - int(gross_metal * tax_rate)
        net_crystal = gross_crystal - int(gross_crystal * tax_rate)
        net_narion = gross_narion - int(gross_narion * tax_rate)

        self.assertEqual(self.planet.net_metal_production, net_metal)
        self.assertEqual(self.planet.net_crystal_production, net_crystal)
        self.assertEqual(self.planet.net_narion_production, net_narion)

    def test_generate_resources(self):
        """Test resource generation and tax payment."""
        initial_metal = self.planet.metal
        initial_crystal = self.planet.crystal
        initial_narion = self.planet.narion

        self.planet.generate_resources()

        # Check that resources were updated
        self.assertGreater(self.planet.metal, initial_metal)
        self.assertGreater(self.planet.crystal, initial_crystal)
        self.assertGreater(self.planet.narion, initial_narion)

    def test_exchange_valid(self):
        """Test valid resource exchange."""
        initial_metal = 100
        initial_narion = 100
        
        self.planet.metal = initial_metal
        self.planet.narion = initial_narion
        self.planet.save()
        
        self.market.metal = 0
        self.market.narion = initial_narion
        self.market.save()

        # Perform an exchange
        self.planet.exchange('metal', 'narion', 100)

        self.planet.refresh_from_db()
        self.market.refresh_from_db()
        
        # Check that resources were exchanged
        self.assertEqual(self.planet.metal, initial_metal - 100)
        self.assertEqual(self.planet.narion, initial_narion * (1+self.market.metal_rate))
        self.assertEqual(self.market.metal, 100)
        self.assertEqual(self.market.narion, initial_narion - initial_narion * self.market.metal_rate)

    def test_exchange_invalid_input(self):
        """Test exchange with invalid input resource."""
        with self.assertRaises(ValueError, msg="Input resource type does not exist!"):
            self.planet.exchange('invalid_input', 'narion', 100)

    def test_exchange_invalid_output(self):
        """Test exchange with invalid output resource."""
        with self.assertRaises(ValueError, msg="Output resource type does not exist!"):
            self.planet.exchange('metal', 'invalid_output', 100)

    def test_exchange_exceeds_market(self):
        """Test exchange when trying to withdraw more from the market than available."""
        initial_metal = 100
        initial_narion = 40

        self.planet.metal = initial_metal
        self.planet.narion = 0

        self.market.metal = 0
        self.market.narion = initial_narion

        self.market.metal_rate = 0.5

        self.planet.save()
        self.market.save()

        # Attempt to exchange for more narion than the market can provide
        self.planet.exchange('metal', 'narion', 100)

        self.planet.refresh_from_db()
        self.market.refresh_from_db()
        
        # Calculate how much metal was actually exchanged
        exchanged_metal = initial_narion / self.market.metal_rate
        

        # Assert that the planet has the correct amount of metal and narion after the exchange
        self.assertEqual(self.planet.metal, initial_metal - exchanged_metal)
        self.assertEqual(self.planet.narion, initial_narion)

        # Assert that the market's narion has been reduced to 0 after the exchange
        self.assertEqual(self.market.narion, 0)
