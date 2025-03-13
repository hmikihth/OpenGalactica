from django.test import TestCase
from django.utils import timezone
from django.template.defaultfilters import slugify
from engine.models import News, Planet

class NewsModelTest(TestCase):
    def setUp(self):
        """Set up a test Planet instance"""
        self.planet = Planet.objects.create(name="TestPlanet")  # Adjust fields as needed

    def test_news_slug_creation(self):
        """Test slug creation from round, turn, and title"""
        news = News.objects.create(
            author=self.planet,
            round=1,
            turn=50,
            title="Test News Title",
            content="<p>This is a test news content.</p>",
        )
        expected_slug = slugify("1-50-Test News Title")  # Ensures consistency
        self.assertEqual(news.slug, expected_slug)
        self.assertEqual(str(news), news.title)

    def test_news_slug_uniqueness(self):
        """Test that duplicate titles generate unique slugs"""
        news1 = News.objects.create(
            author=self.planet,
            round=1,
            turn=50,
            title="Same Title",
            content="<p>First news with same title.</p>",
        )
        news2 = News.objects.create(
            author=self.planet,
            round=1,
            turn=50,
            title="Same Title",
            content="<p>Second news with same title.</p>",
        )

        self.assertNotEqual(news1.slug, news2.slug)
        self.assertTrue(news2.slug.startswith(news1.slug))  # Should append "-1" or higher

    def test_news_description_property(self):
        """Test that description property truncates long content"""
        short_content = "Short news content."
        long_content = "A" * 300  # Simulate long content exceeding 255 characters
        
        news1 = News.objects.create(
            author=self.planet, round=1, turn=50, title="Short Content", content=short_content
        )
        news2 = News.objects.create(
            author=self.planet, round=1, turn=50, title="Long Content", content=long_content
        )

        self.assertEqual(news1.description, short_content)
        self.assertEqual(news2.description, long_content[:255] + "...")

    def test_news_timestamp_property(self):
        """Test timestamp formatting"""
        news = News.objects.create(
            author=self.planet,
            round=3,
            turn=120,
            title="Test Timestamp",
            content="<p>Timestamp test.</p>",
            server_time=timezone.make_aware(timezone.datetime(2025, 3, 7, 14, 45, 30)),  # Fixed time
        )

        self.assertEqual(news.timestamp, "3:120:45")  # Checks round:turn:minute format
