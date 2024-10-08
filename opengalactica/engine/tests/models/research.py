from django.test import TestCase
from engine.models import Research, PlanetResearch, SolResearch, AllianceResearch, Planet, Sol, Alliance

class ResearchTestCase(TestCase):
    def setUp(self):
        # Create Research objects
        self.research1 = Research.objects.create(
            name="Basic Weaponry",
            research_type="Weapon",
            species="Human",
            description="Basic weapons technology.",
            metal=100,
            crystal=50,
            narion=20,
            development_time=5,
            bonus_type="accuracy",
            bonus_value=0.05,
            fine_type="universe speed",
            fine_value=-1
        )

        self.research2 = Research.objects.create(
            name="Advanced Weaponry",
            research_type="Weapon",
            species="Human",
            description="Advanced weapons technology.",
            metal=200,
            crystal=100,
            narion=50,
            development_time=10,
            requirement=self.research1,
            bonus_type="accuracy",
            bonus_value=0.1,
            fine_type="universe speed",
            fine_value=-2
        )

    def test_research_creation(self):
        """Test if research objects are correctly created."""
        self.assertEqual(self.research1.name, "Basic Weaponry")
        self.assertEqual(self.research2.name, "Advanced Weaponry")
        self.assertEqual(self.research2.requirement, self.research1)

    def test_bonus_property(self):
        """Test the bonus property of Research."""
        self.assertEqual(self.research1.bonus, {"accuracy": 0.05})
        self.assertEqual(self.research2.bonus, {"accuracy": 0.1})
        
    def test_fine_property(self):
        """Test the fine property of Research."""
        self.assertEqual(self.research1.fine, {"universe speed": -1})
        self.assertEqual(self.research2.fine, {"universe speed": -2})
        
    def test_research_points(self):
        """Test the points property of the Research model."""        
        expected_points = self.research1.metal + self.research1.crystal + self.research1.narion
        self.assertEqual(self.research1.points, expected_points)


class PlanetResearchTestCase(TestCase):
    def setUp(self):
        # Create Research objects
        self.research1 = Research.objects.create(
            name="Basic Weaponry",
            research_type="Weapon",
            species="Human",
            description="Basic weapons technology.",
            metal=100,
            crystal=50,
            narion=20,
            development_time=5
        )

        self.research2 = Research.objects.create(
            name="Advanced Weaponry",
            research_type="Weapon",
            species="Human",
            description="Advanced weapons technology.",
            metal=200,
            crystal=100,
            narion=50,
            development_time=10,
            requirement=self.research1
        )

        # Create a mock planet
        self.planet = Planet.objects.create(
            name="Test Planet", x=0, y=0, z=0
        )

        # Create PlanetResearch objects
        self.planet_research1 = PlanetResearch.objects.create(
            planet=self.planet,
            research=self.research1
        )

        self.planet_research2 = PlanetResearch.objects.create(
            planet=self.planet,
            research=self.research2
        )

    def test_planet_research_creation(self):
        """Test if PlanetResearch objects are correctly created."""
        self.assertEqual(self.planet_research1.research.name, "Basic Weaponry")
        self.assertEqual(self.planet_research1.turns_remaining, 5)
        self.assertFalse(self.planet_research1.completed)

    def test_start_research(self):
        """Test the start_research method to decrease turns and complete research."""
        self.planet_research1.start_research()
        self.assertEqual(self.planet_research1.turns_remaining, 4)
        self.assertFalse(self.planet_research1.completed)

        # Complete the research
        self.planet_research1.turns_remaining = 1
        self.planet_research1.start_research()
        self.assertEqual(self.planet_research1.turns_remaining, 0)
        self.assertTrue(self.planet_research1.completed)

    def test_can_start_research(self):
        """Test the can_start method to verify prerequisite research is completed."""
        # Should be able to start research1 since it has no prerequisite
        self.assertTrue(self.planet_research1.can_start())

        # Cannot start research2 until research1 is completed
        self.assertFalse(self.planet_research2.can_start())

        # Mark research1 as completed and verify research2 can now be started
        self.planet_research1.completed = True
        self.planet_research1.save()
        self.assertTrue(self.planet_research2.can_start())

    def test_exclusive_group_restriction(self):
        """Test that exclusive group restriction prevents starting multiple researches."""
        research_exclusive_1 = Research.objects.create(
            name="Defense Tech A",
            research_type="Defense",
            species="Human",
            description="Defense tech A.",
            metal=150,
            crystal=100,
            narion=75,
            development_time=6,
            exclusive_group="defense_group"
        )
        
        research_exclusive_2 = Research.objects.create(
            name="Defense Tech B",
            research_type="Defense",
            species="Human",
            description="Defense tech B.",
            metal=200,
            crystal=150,
            narion=50,
            development_time=6,
            exclusive_group="defense_group"
        )

        # Start the first research
        planet_research_excl_1 = PlanetResearch.objects.create(
            planet=self.planet,
            research=research_exclusive_1,
            started=True
        )
        
        # Try to start the second exclusive research
        planet_research_excl_2 = PlanetResearch.objects.create(
            planet=self.planet,
            research=research_exclusive_2
        )
        
        # Should not be allowed to start because of the exclusive group conflict
        self.assertFalse(planet_research_excl_2.can_start())
        

class SolResearchTestCase(TestCase):
    def setUp(self):
        # Create Research and Sol objects
        self.research1 = Research.objects.create(
            name="Sol Weaponry",
            research_type="Weapon",
            species="Sol",
            description="Sol weapon technology.",
            metal=300,
            crystal=200,
            narion=100,
            development_time=7
        )

        self.sol = Sol.objects.create(name="Test Sol")

        # Create SolResearch objects
        self.sol_research1 = SolResearch.objects.create(
            sol=self.sol,
            research=self.research1
        )

    def test_sol_research_creation(self):
        """Test if SolResearch objects are correctly created."""
        self.assertEqual(self.sol_research1.research.name, "Sol Weaponry")
        self.assertEqual(self.sol_research1.turns_remaining, 7)
        self.assertFalse(self.sol_research1.completed)

    def test_exclusive_group_restriction(self):
        """Test that exclusive group restriction prevents starting multiple researches."""
        research_exclusive_1 = Research.objects.create(
            name="Sol Defense A",
            research_type="Defense",
            species="Sol",
            description="Defense tech A.",
            metal=200,
            crystal=150,
            narion=75,
            development_time=8,
            exclusive_group="sol_defense_group"
        )

        research_exclusive_2 = Research.objects.create(
            name="Sol Defense B",
            research_type="Defense",
            species="Sol",
            description="Defense tech B.",
            metal=250,
            crystal=200,
            narion=100,
            development_time=8,
            exclusive_group="sol_defense_group"
        )

        # Start the first research
        sol_research_excl_1 = SolResearch.objects.create(
            sol=self.sol,
            research=research_exclusive_1,
            started=True
        )
        
        # Try to start the second exclusive research
        sol_research_excl_2 = SolResearch.objects.create(
            sol=self.sol,
            research=research_exclusive_2
        )

        # Should not be allowed to start because of the exclusive group conflict
        self.assertFalse(sol_research_excl_2.can_start())


class AllianceResearchTestCase(TestCase):
    def setUp(self):
        # Create Research and Alliance objects
        self.research1 = Research.objects.create(
            name="Alliance Weaponry",
            research_type="Weapon",
            species="Alliance",
            description="Alliance weapon technology.",
            metal=500,
            crystal=300,
            narion=200,
            development_time=9
        )

        self.alliance = Alliance.objects.create(name="Test Alliance")

        # Create AllianceResearch objects
        self.alliance_research1 = AllianceResearch.objects.create(
            alliance=self.alliance,
            research=self.research1
        )

    def test_alliance_research_creation(self):
        """Test if AllianceResearch objects are correctly created."""
        self.assertEqual(self.alliance_research1.research.name, "Alliance Weaponry")
        self.assertEqual(self.alliance_research1.turns_remaining, 9)
        self.assertFalse(self.alliance_research1.completed)

    def test_exclusive_group_restriction(self):
        """Test that exclusive group restriction prevents starting multiple researches."""
        research_exclusive_1 = Research.objects.create(
            name="Alliance Defense A",
            research_type="Defense",
            species="Alliance",
            description="Alliance defense tech A.",
            metal=400,
            crystal=250,
            narion=150,
            development_time=8,
            exclusive_group="alliance_defense_group"
        )

        research_exclusive_2 = Research.objects.create(
            name="Alliance Defense B",
            research_type="Defense",
            species="Alliance",
            description="Alliance defense tech B.",
            metal=450,
            crystal=300,
            narion=200,
            development_time=8,
            exclusive_group="alliance_defense_group"
        )

        # Start the first exclusive research
        alliance_research_excl_1 = AllianceResearch.objects.create(
            alliance=self.alliance,
            research=research_exclusive_1,
            started=True
        )

        # Try to start the second exclusive research
        alliance_research_excl_2 = AllianceResearch.objects.create(
            alliance=self.alliance,
            research=research_exclusive_2
        )

        # Should not be allowed to start because of the exclusive group conflict
        self.assertFalse(alliance_research_excl_2.can_start())

