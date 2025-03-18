from django.test import TestCase
from django.utils import timezone
from engine.models import Planet, Notification

class NotificationModelTest(TestCase):
    def setUp(self):
        self.planet = Planet.objects.create(name="Test Planet")
    
    def test_create_notification(self):
        notification = Notification.objects.create(
            planet=self.planet,
            round=1,
            turn=5,
            ntype="War",
            content="A battle has begun!"
        )
        
        self.assertEqual(notification.planet, self.planet)
        self.assertEqual(notification.round, 1)
        self.assertEqual(notification.turn, 5)
        self.assertEqual(notification.ntype, "War")
        self.assertEqual(notification.content, "A battle has begun!")
        self.assertFalse(notification.read)
        self.assertIsNotNone(notification.server_time)
    
    def test_default_read_status(self):
        notification = Notification.objects.create(
            planet=self.planet,
            round=2,
            turn=10,
            ntype="Research",
            content="New technology discovered!"
        )
        self.assertFalse(notification.read)
    
    def test_mark_notification_as_read(self):
        notification = Notification.objects.create(
            planet=self.planet,
            round=3,
            turn=15,
            ntype="Building",
            content="A new structure has been completed!"
        )
        
        notification.read = True
        notification.save()
        
        updated_notification = Notification.objects.get(id=notification.id)
        self.assertTrue(updated_notification.read)
