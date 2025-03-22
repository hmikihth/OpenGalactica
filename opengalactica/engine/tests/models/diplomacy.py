from django.core.exceptions import ValidationError
from django.test import TestCase
from engine.models import Diplomacy, Alliance

class DiplomacyTestCase(TestCase):
    def setUp(self):
        self.alliance1 = Alliance.objects.create(name="Alliance One")
        self.alliance2 = Alliance.objects.create(name="Alliance Two")

    def test_create_diplomacy(self):
        diplomacy = Diplomacy.objects.create(
            sender=self.alliance1,
            receiver=self.alliance2,
            diplo_type="Ally",
            expiration=150,
            termination=20,
            description="Strategic partnership."
        )
        self.assertEqual(diplomacy.sender, self.alliance1)
        self.assertEqual(diplomacy.receiver, self.alliance2)
        self.assertEqual(diplomacy.diplo_type, "Ally")
        self.assertEqual(diplomacy.expiration, 150)
        self.assertEqual(diplomacy.termination, 20)
        self.assertEqual(diplomacy.description, "Strategic partnership.")
        self.assertFalse(diplomacy.accepted, "New diplomacy must not be accepted by default")

    def test_accept_diplomacy(self):
        diplomacy = Diplomacy.objects.create(
            sender=self.alliance1,
            receiver=self.alliance2,
            diplo_type="Trade",
            expiration=100,
            termination=15
        )
        diplomacy.accept()
        self.assertTrue(diplomacy.accepted, "Diplomacy should be accepted after calling the accept method")

    def test_unique_diplomacy(self):
        Diplomacy.objects.create(
            sender=self.alliance1,
            receiver=self.alliance2,
            diplo_type="Neutral",
            expiration=150,
            termination=10
        )
        with self.assertRaises(ValidationError):
            duplicate_diplomacy = Diplomacy(
                sender=self.alliance1,
                receiver=self.alliance2,
                diplo_type="Neutral",
                expiration=200,
                termination=15
            )
            duplicate_diplomacy.full_clean()  # This should raise a validation error
