"""
Test for Users API
"""


from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status


REGISTER_USER_URL = reverse('user:register')
TOKEN_URL = reverse('user:token')
PROFILE_USER = reverse('user:profile')


def create_user(**params):
    """Create new user and return"""
    return get_user_model().objects.create_user(**params)


class PublicUser(TestCase):
    """Test public user"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test create user success"""
        data = {
            'email': 'usertest@example.com',
            'password': '123password',

        }
        response = self.client.post(REGISTER_USER_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=data['email'])
        self.assertTrue(user.check_password(data['password']))
        self.assertNotIn('password', response.data)

    def test_user_email_already_exists(self):
        """Test returned error if email exists"""
        data = {
            'email': 'usertest1@example.com',
            'password': '123password',

        }
        create_user(**data)

        response = self.client.post(REGISTER_USER_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_password_too_short(self):
        """Test if password is too short"""
        data = {
            'email': 'usertest@example.com',
            'password': '123',

        }
        response = self.client.post(REGISTER_USER_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_test = get_user_model().objects.filter(
            email=data['email']
        ).exists()
        self.assertFalse(user_test)

    def test_access_token_user(self):
        """Test valid credentials for generate token access"""
        test_user = {
            'email': 'usertest@example.com',
            'password': '123password',
        }
        create_user(**test_user)

        data_user = {
            'email': test_user['email'],
            'password': test_user['password'],
        }
        response = self.client.post(TOKEN_URL, data_user)

        self.assertIn('access', response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_token_user_unauthorized(self):
        """Test unauthorized for invalid credentials"""
        test_user = {
            'email': 'usertest@example.com',
            'password': '123password',
        }
        create_user(**test_user)
        data_user = {
            'email': 'usertestBAD@example.com',
            'password': '123password'
        }
        response = self.client.post(TOKEN_URL, data_user)

        self.assertNotIn('access', response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
