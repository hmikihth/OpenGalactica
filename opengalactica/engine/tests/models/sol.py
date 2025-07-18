from django.test import TestCase
from engine.models import Sol, Planet, CommanderVote, OutVote, PlanetRelocation

class SolTestCase(TestCase):
    def setUp(self):
        """Set up the initial state with a sol and planets."""
        self.planet1 = Planet.objects.create(name="Planet1")
        self.planet2 = Planet.objects.create(name="Planet2")
        self.planet3 = Planet.objects.create(name="Planet3")
        self.sol = Sol.objects.create(name="Test Sol", x=4, y=3)
        self.sol.add_planet(self.planet1)
        self.sol.add_planet(self.planet2)
        self.sol.add_planet(self.planet3)

    def test_add_planet(self):
        """Test that a planet can be added to a sol if it is not full."""
        self.sol = Sol.objects.create(name="Test Sol", x=4, y=2)
        self.sol.add_planet(self.planet1)
        self.assertEqual(self.planet1.sol, self.sol)

    def test_add_planet_sol_full(self):
        """Test that an error is raised if the sol is full."""
        self.sol = Sol.objects.create(name="Test Sol", x=4, y=1)
        for i in range(1, 11):  # Fill up the sol with 10 planets
            planet = Planet.objects.create(name=f"Planet{i}")
            self.sol.add_planet(planet)

        with self.assertRaises(ValueError, msg="The sol is full"):
            self.sol.add_planet(self.planet1)

    def test_planet_relocations_count(self):
        """Test that the relocation count in a sol is correct."""
        PlanetRelocation.objects.create(planet=self.planet1, sol=self.sol, invitation=False)
        PlanetRelocation.objects.create(planet=self.planet2, sol=self.sol, invitation=False)
        self.assertEqual(self.sol.n_relocations, 2)

    def test_commander_vote(self):
        """Test that the commander can be voted and set correctly."""
        self.sol.send_vote_commander(self.planet1, self.planet2)
        self.assertEqual(self.sol.commander, self.planet1)

    def test_vote_outvote(self):
        """Test that outvotes are processed correctly."""
        self.sol.send_vote_outvote(self.planet1, self.planet2, value=True)
        self.sol.send_vote_outvote(self.planet1, self.planet3, value=True)
        self.assertTrue(self.sol.is_outvoted(self.planet1))

class SolXPAndPointsTests(TestCase):
    
    def setUp(self):
        # Create a Sol instance
        self.sol = Sol.objects.create(name="Test Sol", x=2, y=3)
        
        # Create some Planet instances and associate them with the Sol
        self.planet1 = Planet.objects.create(name="Planet 1", x=2, y=3, z=1, xp=100, points=200)
        self.planet2 = Planet.objects.create(name="Planet 2", x=2, y=3, z=2, xp=150, points=250)
        self.planet3 = Planet.objects.create(name="Planet 3", x=2, y=3, z=3, xp=200, points=300)

    def test_xp(self):
        # Check that the sol's xp is the sum of its planets' xp
        total_xp = self.planet1.xp + self.planet2.xp + self.planet3.xp
        self.sol.recount_xp()
        self.assertEqual(self.sol.xp, total_xp)

        self.planet1.xp += 100
        self.planet1.save()
        self.sol.recount_xp()
        self.assertEqual(self.sol.xp, total_xp+100)
        self.assertEqual(self.sol.xp_before, total_xp)

    def test_points(self):
        # Check that the sol's points is the sum of its planets' points
        total_points = self.planet1.points + self.planet2.points + self.planet3.points
        self.sol.recount_points()
        self.assertEqual(self.sol.points, total_points)

        self.planet1.points += 100
        self.planet1.save()
        self.sol.recount_points()
        self.assertEqual(self.sol.points, total_points+100)
        self.assertEqual(self.sol.points_before, total_points)

    def test_xp_no_planets(self):
        # Create a new sol with no planets
        empty_sol = Sol.objects.create(name="Empty Sol", x=3, y=4)
        self.sol.recount_xp()
        self.assertEqual(empty_sol.xp, 0)

    def test_points_no_planets(self):
        # Create a new sol with no planets
        empty_sol = Sol.objects.create(name="Empty Sol", x=3, y=4)
        self.sol.recount_points()
        self.assertEqual(empty_sol.points, 0)
        
        
class CommanderVoteTestCase(TestCase):
    def setUp(self):
        """Set up a commander vote test with a sol and planets."""
        self.sol = Sol.objects.create(name="Sol Vote", x=3, y=2)
        self.planet1 = Planet.objects.create(name="Planet1")
        self.planet2 = Planet.objects.create(name="Planet2")
        self.sol.add_planet(self.planet1)
        self.sol.add_planet(self.planet2)

    def test_commander_vote_creation(self):
        """Test the creation of a commander vote."""
        CommanderVote.objects.create(sol=self.sol, planet=self.planet1, voter=self.planet2)
        self.assertEqual(CommanderVote.objects.count(), 1)

    def test_set_commander(self):
        """Test setting a commander based on votes."""
        CommanderVote.objects.create(sol=self.sol, planet=self.planet1, voter=self.planet2)
        self.sol.set_commander()
        self.assertEqual(self.sol.commander, self.planet1)


class OutVoteTestCase(TestCase):
    def setUp(self):
        """Set up outvote test with a sol and planets."""
        self.sol = Sol.objects.create(name="OutVote Sol", x=2, y=1)
        self.planet1 = Planet.objects.create(name="Planet1")
        self.planet2 = Planet.objects.create(name="Planet2")
        self.sol.add_planet(self.planet1)
        self.sol.add_planet(self.planet2)

    def test_outvote_creation(self):
        """Test the creation of an outvote."""
        OutVote.objects.create(sol=self.sol, planet=self.planet1, voter=self.planet2, value=True)
        self.assertEqual(OutVote.objects.count(), 1)

    def test_send_outvote(self):
        """Test sending an outvote and checking if a planet is outvoted."""
        self.sol.send_vote_outvote(self.planet1, self.planet2, value=True)
        self.assertTrue(self.sol.is_outvoted(self.planet1))


class SolMinistersMessageTest(TestCase):
    def setUp(self):
        # Create Sol instance
        self.sol = Sol.objects.create(name="Test Sol", ministers_message="Initial Message", x=3, y=3)

        # Create a commander planet
        self.commander = Planet.objects.create(name="Commander Planet")
        self.sol.add_planet(self.commander)
        self.sol.commander = self.commander
        
        # Create a minister of war planet
        self.minister_of_war = Planet.objects.create(name="Minister Planet")
        self.sol.add_planet(self.minister_of_war)
        self.sol.minister_of_war = self.minister_of_war
        
        # Create an unauthorized planet
        self.unauthorized_planet = Planet.objects.create(name="Unauthorized Planet")
        
    
    def test_commander_can_set_ministers_message(self):
        self.sol.set_ministers_message(self.commander, "New Message from Commander")
        self.assertEqual(self.sol.ministers_message, "New Message from Commander")
    
    def test_minister_of_war_can_set_ministers_message(self):
        self.sol.set_ministers_message(self.minister_of_war, "New Message from Minister")
        self.assertEqual(self.sol.ministers_message, "New Message from Minister")
    
    def test_unauthorized_planet_cannot_set_ministers_message(self):
        with self.assertRaises(PermissionError):
            self.sol.set_ministers_message(self.unauthorized_planet, "Unauthorized Message")
    
    def test_ministers_message_persistence(self):
        self.sol.set_ministers_message(self.commander, "Persistent Message")
        self.sol.refresh_from_db()
        self.assertEqual(self.sol.ministers_message, "Persistent Message")
        
from engine.models import Fleet

class SolFleetMovementTestCase(TestCase):
    def setUp(self):
        self.sol = Sol.objects.create(name="Fleet Sol", x=1, y=1)
        self.planet1 = Planet.objects.create(name="P1")
        self.planet2 = Planet.objects.create(name="P2")
        self.planet3 = Planet.objects.create(name="P3")
        self.sol.add_planet(self.planet1)
        self.sol.add_planet(self.planet2)

    def test_incoming_and_outgoing_fleets(self):
        # Create a fleet from planet1 (owner) to planet3 (target)
        fleet1 = Fleet.objects.create(owner=self.planet1, task="move", target=self.planet3)
        # Create a fleet from planet3 (owner) to planet2 (target)
        fleet2 = Fleet.objects.create(owner=self.planet3, task="move", target=self.planet2)
        # Create a fleet from planet1 with no target
        fleet3 = Fleet.objects.create(owner=self.planet1)

        self.assertIn(fleet1, self.sol.outgoing_fleets)
        self.assertIn(fleet2, self.sol.incoming_fleets)
        self.assertNotIn(fleet3, self.sol.outgoing_fleets)
        self.assertNotIn(fleet3, self.sol.incoming_fleets)
