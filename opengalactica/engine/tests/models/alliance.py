from django.test import TestCase
from engine.models import Alliance, Planet, Round, AllianceTreasuryLog, AllianceRank

class AllianceTestCase(TestCase):
    fixtures = ["planets", "round", "ranks"]

    def setUp(self):
        """Set up test data."""
        self.alliance = Alliance.objects.get(name="Test Alliance 1")
        self.planet = Planet.objects.get(name="Test Planet 1")
        self.round = Round.objects.first()
        
    def test_creation_with_founder(self):
        planet = Planet.objects.get(name="Test Planet 2")
        alliance = Alliance.objects.create(name="Founded Alliance", identifier="FA", founder=planet)
        self.assertEqual(planet.alliance, alliance, "The planet should be a member of the alliance")
        self.assertEqual(alliance.founder, planet, "The planet should be the founder of the alliance")
        self.assertTrue(planet.rank.is_founder, "The planet sould have a founder rank in the alliance")

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
        
        
class AllianceFounderTestCase(TestCase):
    fixtures = ["ranks", "round"]

    def setUp(self):
        """Set up test data for planets, alliances, ranks, and members."""
        self.planet1 = Planet.objects.create(name="Planet 1")
        self.planet2 = Planet.objects.create(name="Planet 2")
        self.planet3 = Planet.objects.create(name="Planet 3")
        
        self.rank_founder = AllianceRank.objects.get(alliance_type="standard", is_founder=True)
        self.rank_treasurer = AllianceRank.objects.get(name="Treasurer")

        self.alliance = Alliance.objects.create(
            name="Test Alliance",
            identifier="TST01",
            founder=self.planet1,
        )

        self.planet1.alliance=self.alliance
        self.planet1.rank=self.rank_founder
        self.planet2.alliance=self.alliance
        self.planet2.rank=self.rank_treasurer
        self.planet3.alliance=self.alliance
        self.planet3.rank=None
        self.planet1.save()
        self.planet2.save()
        self.planet3.save()

    def test_set_new_founder(self):
        """Test the set_new_founder method assigns a new founder when the current one leaves."""
        
        # Simulate the current founder (planet1) leaving the alliance
        self.planet1.leave_alliance()
        
        self.planet1.refresh_from_db()
        self.alliance.refresh_from_db()
        

        # Check if a new founder was set based on the sorting criteria
        self.assertEqual(self.alliance.founder, self.planet2, "Planet 2 should become the new founder as it meets the criteria.")

        # Ensure the new founder has the founder rank
        self.assertEqual(self.alliance.founder.rank, self.rank_founder, "The new founder should have the 'founder' rank.")

    def test_save_method_with_founder(self):
        """Test the save method assigns a founder and member on alliance creation."""


        # Create a new alliance with a specific founder        
        new_alliance = Alliance.objects.create(
            name="New Alliance",
            identifier="NEW01",
            founder=self.planet3
        )
        self.planet3.refresh_from_db()

        # Verify that the founder is correctly assigned
        self.assertEqual(new_alliance.founder, self.planet3, "The founder should be Planet 3.")
        
        # Verify the new founder is a member with the correct rank
        self.assertEqual(self.planet3.alliance, new_alliance, "Planet 3 should be a member of the new alliance.")
        self.assertEqual(self.planet3.rank, self.rank_founder, "Planet 3 should have the founder rank in the new alliance.")

    def test_save_method_without_founder(self):
        """Test the save method when no founder is provided."""
        # Create a new alliance without specifying a founder
        new_alliance = Alliance(
            name="No Founder Alliance",
            identifier="NF001",
        )
        new_alliance.save()

        # Ensure that the alliance is saved without errors
        self.assertIsNotNone(new_alliance.pk, "Alliance should be saved without a founder.")

    def test_set_new_founder_with_no_members(self):
        """Test that set_new_founder does nothing if there are no members."""
        # Create an empty alliance with no members
        empty_alliance = Alliance.objects.create(name="Empty Alliance", identifier="EA001")

        # Set new founder on an alliance with no members
        new_founder = empty_alliance.set_new_founder()

        # Ensure that no founder is set and no errors occur
        self.assertIsNone(new_founder, "No founder should be assigned when there are no members in the alliance.")

    def test_save_method_updates_existing_member(self):
        """Test that the save method updates the rank of an existing member when setting as founder."""
        # Change the founder of the alliance to another member
        self.alliance.set_new_founder(self.planet2)
        self.alliance.save()

        # Check that Planet 2 is now the founder
        self.assertEqual(self.alliance.founder, self.planet2, "Planet 2 should now be the founder.")

        # Ensure Planet 2's rank was updated to 'founder'
        self.assertEqual(self.planet2.rank, self.rank_founder, "Planet 2's rank should be updated to founder.")

    def test_founder_is_not_overwritten_on_save(self):
        """Test that the founder is not overwritten during a regular save operation."""
        # Call save without passing a new founder
        self.alliance.save()

        # Ensure the founder hasn't changed
        self.assertEqual(self.alliance.founder, self.planet1, "The founder should not be overwritten if not explicitly changed.")
