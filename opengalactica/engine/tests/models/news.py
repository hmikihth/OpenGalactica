from django.test import TestCase
from django.utils import timezone
from engine.models import News, Planet

class NewsModelTest(TestCase):
    def setUp(self):
        self.planet = Planet.objects.create(name="TestPlanet")

    def test_news_slug_creation(self):
        news = News.objects.create(
            author=self.planet,
            round=1,
            turn=50,
            title="Test News Title",
            content="<p>This is a test news content.</p>",
        )
        self.assertEqual(news.slug, "1-50-test-news-title")
        self.assertEqual(str(news), news.title)

    def test_news_slug_uniqueness(self):
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
