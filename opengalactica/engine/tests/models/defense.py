from django.db.utils import IntegrityError
from django.test import TestCase
from engine.models import Planet, Alliance, Defense, DefenseTarget

class DefenseModelsTest(TestCase):
    def setUp(self):
        self.alliance = Alliance.objects.create(name="Test Alliance")
        self.planet1 = Planet.objects.create(name="Planet1", alliance=self.alliance)
        self.planet2 = Planet.objects.create(name="Planet2")
        self.defense = Defense.objects.create(
            organizer=self.planet1,
            alliance=self.alliance,
            short_description="Test Defense",
            description="A test defense",
            arrival=200,
        )
        self.defense_target = DefenseTarget.objects.create(
            defense=self.defense, target=self.planet2, description="Defending Planet2"
        )

    def test_defense_creation(self):
        self.assertEqual(self.defense.organizer, self.planet1)
        self.assertEqual(self.defense.alliance, self.alliance)
        self.assertEqual(self.defense.arrival, 200)

    def test_defense_target_creation(self):
        self.assertEqual(self.defense_target.defense, self.defense)
        self.assertEqual(self.defense_target.target, self.planet2)

    def test_add_target_method(self):
        new_target = Planet.objects.create(name="Planet3")
        self.defense.add_target(new_target, "New defense target")
        
        defense_target = DefenseTarget.objects.get(defense=self.defense, target=new_target)
        self.assertIsNotNone(defense_target)
        self.assertEqual(defense_target.description, "New defense target")

    def test_unique_defense_target_constraint(self):
        """Test that a DefenseTarget cannot be created with the same defense and target"""
        with self.assertRaises(IntegrityError):
            DefenseTarget.objects.create(
                defense=self.defense, target=self.planet2, description="Duplicate defense target"
            )
