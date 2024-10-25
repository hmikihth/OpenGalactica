from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Permission
from engine.models import Planet, News, Round

class NewsViewSetTests(APITestCase):
    
    def setUp(self):
        self.round = Round.objects.create(number=1, turn=1)
        
        # Create users
        self.user_with_permission = User.objects.create_user(username='author', password='pass')
        self.user_without_permission = User.objects.create_user(username='regular', password='pass')
        
        # Create planet for user
        self.planet = Planet.objects.create(user=self.user_with_permission, name="Planet X")
        
        # Grant 'add_news' permission to the first user
        permission = Permission.objects.get(codename='add_news')
        self.user_with_permission.user_permissions.add(permission)
        
        # Create a news instance
        self.news = News.objects.create(
            author=self.planet,
            round=1,
            turn=1,
            title="Test News",
            content="This is a test news article.",
            slug="1-1-test-news"
        )

    def test_public_can_list_news(self):
        """Test that any user can list news"""
        url = '/api/v1/news/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_public_can_retrieve_news(self):
        """Test that any user can retrieve a specific news item by slug"""
        url = f'/api/v1/news/{self.news.slug}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.news.title)

    def test_user_with_permission_can_create_news(self):
        """Test that a user with permission can create news"""
        self.client.login(username='author', password='pass')
        url = '/api/v1/news/'
        data = {
            'title': 'New News Title',
            'content': 'New news content.',
            'round': 1,
            'turn': 2,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(News.objects.count(), 2)

    def test_user_without_permission_cannot_create_news(self):
        """Test that a user without permission cannot create news"""
        self.client.login(username='regular', password='pass')
        url = f'/api/v1/news/{self.news.slug}/'
        data = {
            'title': 'New News Title',
            'content': 'New news content.',
            'round': 1,
            'turn': 2,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_with_permission_can_update_news(self):
        """Test that a user with permission can update news"""
        self.client.login(username='author', password='pass')
        url = f'/api/v1/news/{self.news.slug}/'
        data = {
            'title': 'Updated News Title',
            'content': 'Updated news content.',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.news.refresh_from_db()
        self.assertEqual(self.news.title, 'Updated News Title')

    def test_user_without_permission_cannot_update_news(self):
        """Test that a user without permission cannot update news"""
        self.client.login(username='regular', password='pass')
        url = f'/api/v1/news/{self.news.slug}/'
        data = {
            'title': 'Updated News Title',
            'content': 'Updated news content.',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_with_permission_can_delete_news(self):
        """Test that a user with permission can delete news"""
        self.client.login(username='author', password='pass')
        url = f'/api/v1/news/{self.news.slug}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(News.objects.count(), 0)

    def test_user_without_permission_cannot_delete_news(self):
        """Test that a user without permission cannot delete news"""
        self.client.login(username='regular', password='pass')
        url = f'/api/v1/news/{self.news.slug}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(News.objects.count(), 1)


#from django.urls import reverse
#from rest_framework import status
#from rest_framework.test import APITestCase
#from django.contrib.auth.models import User
from engine.models import Encyclopedia

class EncyclopediaViewSetTests(APITestCase):

    def setUp(self):
        self.round = Round.objects.create(number=1, turn=1)

        # Create users
        self.admin_user = User.objects.create_superuser(username='admin', password='pass')
        self.regular_user = User.objects.create_user(username='user', password='pass')

        # Create an encyclopedia entry
        self.encyclopedia = Encyclopedia.objects.create(
            title="Test Entry",
            content="<p>Test content</p>",
            slug="test-entry"
        )

    def test_public_can_list_encyclopedia(self):
        """Test that any user can list encyclopedia entries"""
        url = '/api/v1/encyclopedia/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_public_can_retrieve_encyclopedia(self):
        """Test that any user can retrieve a specific encyclopedia entry by slug"""
        url = f'/api/v1/encyclopedia/{self.encyclopedia.slug}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.encyclopedia.title)

    def test_admin_can_create_encyclopedia(self):
        """Test that an admin user can create encyclopedia entries"""
        self.client.login(username='admin', password='pass')
        url = '/api/v1/encyclopedia/'
        data = {
            'title': 'New Encyclopedia Entry',
            'content': '<p>New content</p>',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Encyclopedia.objects.count(), 2)

    def test_regular_user_cannot_create_encyclopedia(self):
        """Test that a non-admin user cannot create encyclopedia entries"""
        self.client.login(username='user', password='pass')
        url = '/api/v1/encyclopedia/'
        data = {
            'title': 'New Encyclopedia Entry',
            'content': '<p>New content</p>',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_encyclopedia(self):
        """Test that an admin user can update encyclopedia entries"""
        self.client.login(username='admin', password='pass')
        url = f'/api/v1/encyclopedia/{self.encyclopedia.slug}/'
        data = {
            'title': 'Updated Entry',
            'content': '<p>Updated content</p>',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.encyclopedia.refresh_from_db()
        self.assertEqual(self.encyclopedia.title, 'Updated Entry')

    def test_regular_user_cannot_update_encyclopedia(self):
        """Test that a non-admin user cannot update encyclopedia entries"""
        self.client.login(username='user', password='pass')
        url = f'/api/v1/encyclopedia/{self.encyclopedia.slug}/'
        data = {
            'title': 'Updated Entry',
            'content': '<p>Updated content</p>',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_encyclopedia(self):
        """Test that an admin user can delete encyclopedia entries"""
        self.client.login(username='admin', password='pass')
        url = f'/api/v1/encyclopedia/{self.encyclopedia.slug}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Encyclopedia.objects.count(), 0)

    def test_regular_user_cannot_delete_encyclopedia(self):
        """Test that a non-admin user cannot delete encyclopedia entries"""
        self.client.login(username='user', password='pass')
        url = f'/api/v1/encyclopedia/{self.encyclopedia.slug}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Encyclopedia.objects.count(), 1)

