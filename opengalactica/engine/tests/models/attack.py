from django.test import TestCase
from engine.models import Planet, Alliance, Attack, AttackTarget, AttackSubscription

class AttackModelsTest(TestCase):
    def setUp(self):
        self.alliance = Alliance.objects.create(name="Test Alliance")
        self.planet1 = Planet.objects.create(name="Planet1", alliance=self.alliance)
        self.planet2 = Planet.objects.create(name="Planet2")
        self.attack = Attack.objects.create(
            organizer=self.planet1,
            alliance=self.alliance,
            short_description="Test Attack",
            description="A test attack",
            start=100,
        )
        self.attack_target = AttackTarget.objects.create(
            attack=self.attack, target=self.planet2, description="Targeting Planet2"
        )
        self.subscription = AttackSubscription.objects.create(
            attack_target=self.attack_target, subscriber=self.planet1, note="Joining the attack"
        )

    def test_attack_creation(self):
        self.assertEqual(self.attack.organizer, self.planet1)
        self.assertEqual(self.attack.alliance, self.alliance)

    def test_attack_target_creation(self):
        self.assertEqual(self.attack_target.attack, self.attack)
        self.assertEqual(self.attack_target.target, self.planet2)

    def test_attack_subscription_creation(self):
        self.assertEqual(self.subscription.attack_target, self.attack_target)
        self.assertEqual(self.subscription.subscriber, self.planet1)

    def test_attack_subscription_deleted_on_alliance_leave(self):
        self.planet1.alliance = None
        self.planet1.save()
        self.assertFalse(AttackSubscription.objects.filter(subscriber=self.planet1).exists())
