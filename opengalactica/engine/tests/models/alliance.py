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


class AlliancePropertyTests(TestCase):
    fixtures = ["planets", "alliances"]

    def setUp(self):
        """Set up test data."""
        self.alliance = Alliance.objects.get(name="Test Alliance 1")
        self.planet1 = Planet.objects.get(name="Test Planet 1")
        self.planet2 = Planet.objects.get(name="Test Planet 2")

        # Assign the planets to the alliance
        self.planet1.alliance = self.alliance
        self.planet1.save()
        self.planet2.alliance = self.alliance
        self.planet2.save()

    def test_members_property(self):
        """Test that the members property returns the correct planets."""
        members = self.alliance.members
        # Check that the returned members are correct
        self.assertIn(self.planet1, members, "Planet 1 should be part of the alliance members.")
        self.assertIn(self.planet2, members, "Planet 2 should be part of the alliance members.")

    def test_n_members_property(self):
        """Test that n_members returns the correct number of planets."""
        self.assertEqual(self.alliance.n_members, 2, "n_members should return the correct number of planets.")

    def test_tax_rate_property(self):
        """Test that the tax_rate property returns the correct tax rate."""
        # Check that the tax rate is calculated correctly (tax/100)
        expected_tax_rate = self.alliance.tax / 100
        self.assertEqual(self.alliance.tax_rate, expected_tax_rate, "The tax rate should be calculated correctly.")
        
        # Test with a tax of 0
        self.alliance.tax = 0
        self.assertEqual(self.alliance.tax_rate, 0, "The tax rate should be 0 when tax is 0.")
        
        # Test with a tax of 100
        self.alliance.tax = 100
        self.assertEqual(self.alliance.tax_rate, 1, "The tax rate should be 1 when tax is 100.")

    def test_xp_property(self):
        """Test that the xp property returns the total xp of all members."""
        # Assume some XP values for the planets
        self.planet1.xp = 100
        self.planet1.save()
        self.planet2.xp = 200
        self.planet2.save()

        total_xp = self.planet1.xp + self.planet2.xp
        self.assertEqual(self.alliance.xp, total_xp, "xp should return the correct sum of xp from all planets.")

    def test_points_property(self):
        """Test that the points property returns the total points of all members."""
        # Assume some point values for the planets
        self.planet1.points = 500
        self.planet1.save()
        self.planet2.points = 700
        self.planet2.save()

        total_points = self.planet1.points + self.planet2.points
        self.assertEqual(self.alliance.points, total_points, "points should return the correct sum of points from all planets.")

    def test_members_with_no_planets(self):
        """Test that members property returns an empty queryset if no planets belong to the alliance."""
        empty_alliance = Alliance.objects.create(name="Empty Alliance", identifier="EA1")
        self.assertEqual(empty_alliance.members.count(), 0, "Members should return an empty queryset if no planets belong to the alliance.")
        
    def test_n_members_with_no_planets(self):
        """Test that n_members property returns 0 if no planets belong to the alliance."""
        empty_alliance = Alliance.objects.create(name="Empty Alliance", identifier="EA1")
        self.assertEqual(empty_alliance.n_members, 0, "n_members should return 0 if no planets belong to the alliance.")

    def test_xp_with_no_planets(self):
        """Test that xp property returns 0 if the alliance has no planets."""
        empty_alliance = Alliance.objects.create(name="Empty Alliance", identifier="EA1")
        self.assertEqual(empty_alliance.xp, 0, "xp should return 0 if the alliance has no planets.")

    def test_points_with_no_planets(self):
        """Test that points property returns 0 if the alliance has no planets."""
        empty_alliance = Alliance.objects.create(name="Empty Alliance", identifier="EA1")
        self.assertEqual(empty_alliance.points, 0, "points should return 0 if the alliance has no planets.")
