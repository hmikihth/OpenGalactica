from django.db import IntegrityError
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

    def test_add_target_method(self):
        new_target = Planet.objects.create(name="Planet3")
        self.attack.add_target(new_target, "New target description")
        
        attack_target = AttackTarget.objects.get(attack=self.attack, target=new_target)
        self.assertIsNotNone(attack_target)
        self.assertEqual(attack_target.description, "New target description")
    
    def test_subscribe_method(self):
        new_subscriber = Planet.objects.create(name="Planet4", alliance=self.alliance)
        self.attack_target.subscribe(new_subscriber, "Ready to join")
        
        subscription = AttackSubscription.objects.get(attack_target=self.attack_target, subscriber=new_subscriber)
        self.assertIsNotNone(subscription)
        self.assertEqual(subscription.note, "Ready to join")

    def test_attack_target_unique_together(self):
        with self.assertRaises(IntegrityError):
            AttackTarget.objects.create(attack=self.attack, target=self.planet2, description="Duplicate Target")

    def test_attack_subscription_unique_together(self):
        with self.assertRaises(IntegrityError):
            AttackSubscription.objects.create(attack_target=self.attack_target, subscriber=self.planet1, note="Duplicate Subscription")
