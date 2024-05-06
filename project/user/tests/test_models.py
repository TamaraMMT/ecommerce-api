"""
Test for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_email(self):
        """Test create user with email"""
        email = "example@example.com"
        password = "passwordtest1"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_email_not_empty(self):
        """Test to show an error if empty"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'pass123')

    def test_superuser_create(self):
        """Test create superuser"""
        user = get_user_model().objects.create_superuser(
            'superusertest@example.com',
            '123pass'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
