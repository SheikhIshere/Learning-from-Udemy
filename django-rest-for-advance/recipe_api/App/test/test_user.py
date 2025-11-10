"""
Testing api of user
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()
CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """create and return new user"""
    return User.objects.create_user(**params)

class PublicUserApiTest(TestCase):
    """test the public features of the user api"""
    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_success(self):
        """test creating user is success full"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

        self.assertNotIn('password', res.data)
    
    def test_user_with_email_exist_error(self):
        """test error if user's email is already exist in data base"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'test name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_is_too_short_error(self):
        """giving error if password is too short ew!!"""
        payload = {
            'email': 'test@example.com',
            'password': 'ew',
            'name': 'test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = User.objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exist)