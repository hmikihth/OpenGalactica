from django.test import TestCase
from engine.models import Research, PlanetResearch, Planet

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
            research=self.research1,
            turns_remaining=5
        )

        self.planet_research2 = PlanetResearch.objects.create(
            planet=self.planet,
            research=self.research2,
            turns_remaining=10
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

    def test_bonus_property(self):
        """Test the bonus property of PlanetResearch."""
        self.assertEqual(self.planet_research1.bonus, {})
        self.research1.bonus_type = "evasion"
        self.research1.bonus_value = 0.05
        self.research1.save()
        self.assertEqual(self.planet_research1.bonus, {"evasion": 0.05})

    def test_fine_property(self):
        """Test the fine property of PlanetResearch."""
        self.assertEqual(self.planet_research1.fine, {})
        self.research1.fine_type = "damage"
        self.research1.fine_value = -1
        self.research1.save()
        self.assertEqual(self.planet_research1.fine, {"damage": -1})

    def test_planet_research_points(self):
        """Test the points property of the PlanetResearch model."""
        planet_research = PlanetResearch.objects.create(
            planet=self.planet,
            research=self.research1,
            turns_remaining=5
        )
        
        self.assertEqual(planet_research.points, self.research1.points)
        
    def test_mutually_exclusive_research(self):
        """Test that mutually exclusive researches cannot be developed at the same time."""
        # Setup two mutually exclusive researches
        research1 = Research.objects.create(
            name="Anti-EMP Shield",
            research_type="Defense",
            species="Human",
            description="Protects against EMP weapons.",
            metal=100,
            crystal=150,
            narion=50,
            development_time=5,
            exclusive_group="defense_choice"
        )
        
        research2 = Research.objects.create(
            name="Self-Destruction Charge",
            research_type="Defense",
            species="Human",
            description="Ships can self-destruct.",
            metal=120,
            crystal=100,
            narion=60,
            development_time=6,
            exclusive_group="defense_choice"
        )

        # Start research1 and complete it
        planet_research1 = PlanetResearch.objects.create(
            planet=self.planet,
            research=research1,
            turns_remaining=0,
            completed=True
        )

        # Attempt to start research2, should return False since research1 is already completed
        planet_research2 = PlanetResearch.objects.create(
            planet=self.planet,
            research=research2,
            turns_remaining=6
        )

        self.assertFalse(planet_research2.can_start())
