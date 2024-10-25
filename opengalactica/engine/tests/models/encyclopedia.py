from django.test import TestCase
from engine.models import Encyclopedia

class EncyclopediaModelTest(TestCase):
    def test_encyclopedia_slug_creation(self):
        entry = Encyclopedia.objects.create(
            title="Test Encyclopedia Entry",
            content="<p>This is test encyclopedia content.</p>",
        )
        self.assertEqual(entry.slug, "test-encyclopedia-entry")
        self.assertEqual(str(entry), entry.title)

    def test_encyclopedia_slug_uniqueness(self):
        entry1 = Encyclopedia.objects.create(
            title="Same Title",
            content="<p>First encyclopedia with same title.</p>",
        )
        entry2 = Encyclopedia.objects.create(
            title="Same Title",
            content="<p>Second encyclopedia with same title.</p>",
        )
        self.assertNotEqual(entry1.slug, entry2.slug)
