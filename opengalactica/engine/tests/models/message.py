from django.test import TestCase
from django.utils import timezone
from engine.models import Message, Planet, Alliance  # Assuming your models are in 'engine'

class MessageModelTest(TestCase):
    def setUp(self):
        self.sender = Planet.objects.create(name="Earth", x=5, y=5, z=1)
        self.receiver = Planet.objects.create(name="Mars", x=5, y=5, z=2)
        self.alliance = Alliance.objects.create(name="Galactic Union")

    def test_create_message(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            round=1,
            turn=5,
            title="Hello World",
            content="This is a test message.",
            alliance=self.alliance
        )
        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.receiver, self.receiver)
        self.assertEqual(message.round, 1)
        self.assertEqual(message.turn, 5)
        self.assertEqual(message.title, "Hello World")
        self.assertEqual(message.content, "This is a test message.")
        self.assertEqual(message.alliance, self.alliance)
        self.assertFalse(message.read)
        self.assertTrue(isinstance(message.server_time, timezone.datetime))

    def test_message_null_sender_receiver(self):
        message = Message.objects.create(
            sender=None,
            receiver=None,
            round=2,
            turn=10,
            title="No Sender or Receiver",
            content="This message has no sender or receiver."
        )
        self.assertIsNone(message.sender)
        self.assertIsNone(message.receiver)

    def test_default_read_value(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            round=3,
            turn=15,
            title="Unread Message",
            content="This should be unread."
        )
        self.assertFalse(message.read)  # Default should be False

    def test_str_representation(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            round=4,
            turn=20,
            title="Test String Representation",
            content="Testing __str__ method."
        )
        self.assertEqual(str(message), "Test String Representation")
