from django.test import TestCase
from engine.models import Alliance, Planet, Round, AllianceTreasuryLog

class AllianceTestCase(TestCase):
    fixtures = ["planets", "round"]

    def setUp(self):
        """Set up test data."""
        self.alliance = Alliance.objects.get(name="Test Alliance 1")
        self.planet = Planet.objects.get(name="Test Planet 1")
        self.round = Round.objects.first()

    def test_pay_tax_updates_alliance_resources(self):
        """Test that pay_tax() correctly updates the alliance's resources."""
        # Initial resources
        initial_metal = self.alliance.metal
        initial_crystal = self.alliance.crystal
        initial_narion = self.alliance.narion

        # Pay tax
        metal_tax = 100
        crystal_tax = 50
        narion_tax = 30
        self.alliance.pay_tax(self.planet, metal_tax, crystal_tax, narion_tax)

        # Refresh from the database to check the updated values
        self.alliance.refresh_from_db()

        # Assert that resources are updated correctly
        self.assertEqual(self.alliance.metal, initial_metal + metal_tax, "Metal should be updated correctly.")
        self.assertEqual(self.alliance.crystal, initial_crystal + crystal_tax, "Crystal should be updated correctly.")
        self.assertEqual(self.alliance.narion, initial_narion + narion_tax, "Narion should be updated correctly.")

    def test_pay_tax_creates_treasury_log(self):
        """Test that pay_tax() correctly creates a new AllianceTreasuryLog entry."""
        # Ensure no logs exist initially
        initial_log_count = AllianceTreasuryLog.objects.count()
        metal_tax = 200
        crystal_tax = 100
        narion_tax = 50

        # Pay tax
        self.alliance.pay_tax(self.planet, metal_tax, crystal_tax, narion_tax)

        # Ensure that a new log entry is created
        log = AllianceTreasuryLog.objects.last()
        self.assertEqual(AllianceTreasuryLog.objects.count(), initial_log_count + 1, "A new treasury log should be created.")
        self.assertEqual(log.alliance, self.alliance, "The log should reference the correct alliance.")
        self.assertEqual(log.planet, self.planet, "The log should reference the correct planet.")
        self.assertEqual(log.turn, self.round.turn, "The log should reference the correct turn.")
        self.assertEqual(log.type, "tax", "The log type should be 'tax'.")
        self.assertEqual(log.metal, metal_tax, "The metal amount in the log should match the tax amount.")
        self.assertEqual(log.crystal, crystal_tax, "The crystal amount in the log should match the tax amount.")
        self.assertEqual(log.narion, narion_tax, "The narion amount in the log should match the tax amount.")

    def test_pay_tax_with_no_planet(self):
        """Test that pay_tax() raises an error if no planet is passed."""
        with self.assertRaises(ValueError, msg="An error should be raised if no planet"):
            self.alliance.pay_tax(None, 100, 50, 25)

    def test_pay_tax_without_round(self):
        """Test that pay_tax() raises an error if no round is available."""
        # Delete all rounds to simulate no round being present
        Round.objects.all().delete()

        with self.assertRaises(ValueError, msg="An error should be raised if no round is available"):
            self.alliance.pay_tax(self.planet, 100, 50, 25)

    def test_pay_tax_with_negative_values(self):
        """Test that pay_tax() raises a ValueError if any tax amount is negative."""
        # Negative metal tax
        with self.assertRaises(ValueError, msg="Negative metal value should raise an error"):
            self.alliance.pay_tax(self.planet, -100, 50, 30)

        # Negative crystal tax
        with self.assertRaises(ValueError, msg="Negative crystal value should raise an error"):
            self.alliance.pay_tax(self.planet, 100, -50, 30)

        # Negative narion tax
        with self.assertRaises(ValueError, msg="Negative narion value should raise an error"):
            self.alliance.pay_tax(self.planet, 100, 50, -30)

    def test_pay_tax_with_zero_values(self):
        """Test that pay_tax() allows zero values for tax amounts."""
        initial_metal = self.alliance.metal
        initial_crystal = self.alliance.crystal
        initial_narion = self.alliance.narion

        # Pay tax with zero values for all resources
        self.alliance.pay_tax(self.planet, 0, 0, 0)

        # Refresh from database and ensure resources remain unchanged
        self.alliance.refresh_from_db()

        self.assertEqual(self.alliance.metal, initial_metal, "Metal should not change if the tax is zero.")
        self.assertEqual(self.alliance.crystal, initial_crystal, "Crystal should not change if the tax is zero.")
        self.assertEqual(self.alliance.narion, initial_narion, "Narion should not change if the tax is zero.")
        
    def test_pay_tax_to_wrong_alliance(self):
        """Test that pay_tax() raises a ValueError if the planet is not a member of the alliance."""
        alliance2 = Alliance("Test Alliance 2", "TA2")
        with self.assertRaises(ValueError, msg="Wrong alliance should raise an error"):
            alliance2.pay_tax(self.planet, 10, 10, 10)
        
        self.planet.alliance = None

        with self.assertRaises(ValueError, msg="Planet without alliance should raise an error"):
            self.alliance.pay_tax(self.planet, 10, 10, 10)
