from django.test import TestCase
from engine.models import Galaxy, Planet, CommanderVote, OutVote, PlanetRelocation

class GalaxyTestCase(TestCase):
    def setUp(self):
        """Set up the initial state with a galaxy and planets."""
        self.planet1 = Planet.objects.create(name="Planet1")
        self.planet2 = Planet.objects.create(name="Planet2")
        self.planet3 = Planet.objects.create(name="Planet3")
        self.galaxy = Galaxy.objects.create(name="Test Galaxy", x=4, y=3)
        self.galaxy.add_planet(self.planet1)
        self.galaxy.add_planet(self.planet2)
        self.galaxy.add_planet(self.planet3)

    def test_add_planet(self):
        """Test that a planet can be added to a galaxy if it is not full."""
        self.galaxy = Galaxy.objects.create(name="Test Galaxy", x=4, y=2)
        self.galaxy.add_planet(self.planet1)
        self.assertEqual(self.planet1.galaxy, self.galaxy)

    def test_add_planet_galaxy_full(self):
        """Test that an error is raised if the galaxy is full."""
        self.galaxy = Galaxy.objects.create(name="Test Galaxy", x=4, y=1)
        for i in range(1, 11):  # Fill up the galaxy with 10 planets
            planet = Planet.objects.create(name=f"Planet{i}")
            self.galaxy.add_planet(planet)

        with self.assertRaises(ValueError, msg="The galaxy is full"):
            self.galaxy.add_planet(self.planet1)

    def test_planet_relocations_count(self):
        """Test that the relocation count in a galaxy is correct."""
        PlanetRelocation.objects.create(planet=self.planet1, galaxy=self.galaxy, invitation=False)
        PlanetRelocation.objects.create(planet=self.planet2, galaxy=self.galaxy, invitation=False)
        self.assertEqual(self.galaxy.n_relocations, 2)

    def test_commander_vote(self):
        """Test that the commander can be voted and set correctly."""
        self.galaxy.send_vote_commander(self.planet1, self.planet2)
        self.assertEqual(self.galaxy.commander, self.planet1)

    def test_vote_outvote(self):
        """Test that outvotes are processed correctly."""
        self.galaxy.send_vote_outvote(self.planet1, self.planet2, value=True)
        self.galaxy.send_vote_outvote(self.planet1, self.planet3, value=True)
        self.assertTrue(self.galaxy.is_outvoted(self.planet1))

class GalaxyXPAndPointsTests(TestCase):
    
    def setUp(self):
        # Create a Galaxy instance
        self.galaxy = Galaxy.objects.create(name="Test Galaxy", x=2, y=3)
        
        # Create some Planet instances and associate them with the Galaxy
        self.planet1 = Planet.objects.create(name="Planet 1", x=2, y=3, z=1, xp=100, points=200)
        self.planet2 = Planet.objects.create(name="Planet 2", x=2, y=3, z=2, xp=150, points=250)
        self.planet3 = Planet.objects.create(name="Planet 3", x=2, y=3, z=3, xp=200, points=300)

    def test_xp_property(self):
        # Check that the galaxy's xp is the sum of its planets' xp
        total_xp = self.planet1.xp + self.planet2.xp + self.planet3.xp
        self.assertEqual(self.galaxy.xp, total_xp)

    def test_points_property(self):
        # Check that the galaxy's points is the sum of its planets' points
        total_points = self.planet1.points + self.planet2.points + self.planet3.points
        self.assertEqual(self.galaxy.points, total_points)

    def test_xp_property_no_planets(self):
        # Create a new galaxy with no planets
        empty_galaxy = Galaxy.objects.create(name="Empty Galaxy", x=3, y=4)
        self.assertEqual(empty_galaxy.xp, 0)

    def test_points_property_no_planets(self):
        # Create a new galaxy with no planets
        empty_galaxy = Galaxy.objects.create(name="Empty Galaxy", x=3, y=4)
        self.assertEqual(empty_galaxy.points, 0)
        
        
class CommanderVoteTestCase(TestCase):
    def setUp(self):
        """Set up a commander vote test with a galaxy and planets."""
        self.galaxy = Galaxy.objects.create(name="Galaxy Vote", x=3, y=2)
        self.planet1 = Planet.objects.create(name="Planet1")
        self.planet2 = Planet.objects.create(name="Planet2")
        self.galaxy.add_planet(self.planet1)
        self.galaxy.add_planet(self.planet2)

    def test_commander_vote_creation(self):
        """Test the creation of a commander vote."""
        CommanderVote.objects.create(galaxy=self.galaxy, planet=self.planet1, voter=self.planet2)
        self.assertEqual(CommanderVote.objects.count(), 1)

    def test_set_commander(self):
        """Test setting a commander based on votes."""
        CommanderVote.objects.create(galaxy=self.galaxy, planet=self.planet1, voter=self.planet2)
        self.galaxy.set_commander()
        self.assertEqual(self.galaxy.commander, self.planet1)


class OutVoteTestCase(TestCase):
    def setUp(self):
        """Set up outvote test with a galaxy and planets."""
        self.galaxy = Galaxy.objects.create(name="OutVote Galaxy", x=2, y=1)
        self.planet1 = Planet.objects.create(name="Planet1")
        self.planet2 = Planet.objects.create(name="Planet2")
        self.galaxy.add_planet(self.planet1)
        self.galaxy.add_planet(self.planet2)

    def test_outvote_creation(self):
        """Test the creation of an outvote."""
        OutVote.objects.create(galaxy=self.galaxy, planet=self.planet1, voter=self.planet2, value=True)
        self.assertEqual(OutVote.objects.count(), 1)

    def test_send_outvote(self):
        """Test sending an outvote and checking if a planet is outvoted."""
        self.galaxy.send_vote_outvote(self.planet1, self.planet2, value=True)
        self.assertTrue(self.galaxy.is_outvoted(self.planet1))