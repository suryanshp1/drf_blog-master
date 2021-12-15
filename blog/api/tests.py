from django.http import response
from django.urls import reverse, resolve
from api.views import PostList
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class PostUrlsTests(APITestCase):
    def test_get_post_is_resolved(self):
        """
        Ensure that URL is resolved.
        """
        url = reverse('posts')
        self.assertEqual(resolve(url).func.view_class, PostList)

class GlobalSetup(APITestCase):
    post_urls = reverse('posts')
    post_url = reverse('posts-detail', args=[5])

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)

        # Saving User
        data = {
            "title": 'Decentralization',
            "body": 'Peer to Peer network is an example of decentralization'
        }
        response = self.client.post(self.post_url, data, format='json')

class PostAPIViewTests(GlobalSetup):

    def test_get_posts_authenticated(self):
        response = self.client.get(self.post_urls)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_posts_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.post_urls)
        self.assertEqual(response.status_code, 200)
    
    def test_post_posts_authenticated(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        data = {
            "title": 'Decentralization',
            "body": 'Peer to Peer network is an example of decentralization'
        }
        response = self.client.post(self.post_urls, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Decentralization')

class PostDetailAPIView(GlobalSetup):

    post_urls = reverse('posts')
    post_url = reverse('posts-detail', args=[5])

    def test_get_post_authenticated(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Decentralization')

    def test_get_post_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.post_urls)
        self.assertEqual(response.status_code, 200)

    def test_delete_post_authenticated(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        response = self.client.delete(self.post_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)