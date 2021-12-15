from django.http import response
from django.urls import reverse, resolve
from api.views import PostList
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Post
import json

class PostUrlsTests(APITestCase):
    def test_get_post_is_resolved(self):
        """
        Ensure that URL is resolved.
        """
        url = reverse('posts')
        self.assertEqual(resolve(url).func.view_class, PostList)

class RegistrationTestCase(APITestCase):
    register = reverse('auth_register')
    def test_registration(self):
        data = {'username': 'testcase', 'first_name': 'Test', 'last_name': 'Man', 'email': 'test@email.com', 'password': 'some_strong_password'}
        response = self.client.post(self.register, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class GlobalSetup(APITestCase):
    post_urls = reverse('posts')
    post_url = reverse('posts-detail', args=[1])

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@123', is_staff=True)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)

        # Saving post

        post_data = Post.objects.create(title="TestTitle", body="Peer to Peer network", owner=self.user)
        
        post_data.save()

        self.post_data = post_data

class PostAPIViewTests(GlobalSetup):
    user_detail = reverse('users-detail', args=[1])
    def test_get_posts_authenticated(self):
        response = self.client.get(self.post_urls)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_posts_un_authenticated(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        response = self.client.get(self.post_urls)
        self.assertEqual(response.status_code, 200)

    def test_user_detail(self):
        response = self.client.get(self.user_detail)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'admin')
    
    def test_post_posts_authenticated(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        data = {
            "title": "Decentralization",
            "body": "Peer to Peer network is an example of decentralization"
        }
        response = self.client.post(self.post_urls, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Decentralization')

    def test_delete_post_authenticated(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        response = self.client.delete(self.post_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_post_authenticated(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        response = self.client.put(self.post_url, {"title": "TestTitle", "body": "Peer to Peer network"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {"id": 1, "title": "TestTitle", "body": "Peer to Peer network", "owner": "admin", "comments": []})