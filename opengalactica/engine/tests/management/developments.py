from django.test import TestCase
from unittest.mock import patch
from engine.models import Planet, Research, PlanetResearch

from engine.management.commands._developments import Developments

class DevelopmentsTestCase(TestCase):
    def setUp(self):
        # Setup the necessary mock objects

        self.research = Research.objects.create(
            name="Basic Weaponry",
            research_type="Weapon",
            species="Human",
            description="Basic weapons technology.",
            metal=100,
            crystal=50,
            narion=20,
            development_time=5
        )


        self.planet = Planet.objects.create(
            name="Test Planet", x=0, y=0, z=5
        )
        self.research1 = PlanetResearch.objects.create(planet=self.planet, research=self.research, turns_remaining=3, completed=False)
        self.research2 = PlanetResearch.objects.create(planet=self.planet, research=self.research, turns_remaining=1, completed=False)

    @patch('engine.models.PlanetResearch.start_research')
    def test_execute_planet_researches(self, mock_start_research):
        """Test that execute_planet_researches calls start_research on each incomplete PlanetResearch."""
        # Create instance of Developments and run
        developments = Developments()
        developments.run()

        # Assert that start_research is called twice (once for each incomplete research)
        self.assertEqual(mock_start_research.call_count, 2)
        mock_start_research.assert_any_call()

    @patch('engine.models.PlanetResearch.start_research')
    def test_run_only_incomplete_research(self, mock_start_research):
        """Test that run only processes incomplete PlanetResearch objects."""
        # Mark one research as completed
        self.research2.completed = True
        self.research2.save()

        # Create instance of Developments and run
        developments = Developments()
        developments.run()

        # Assert that start_research is called only once (for the incomplete research)
        self.assertEqual(mock_start_research.call_count, 1)
        mock_start_research.assert_any_call()
