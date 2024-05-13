"""
Test for admin modifications
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTest(TestCase):
    """Test Django Admin"""

    def setUp(self):
        """Create user and client"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="exampleadmin@example.com",
            password="123password",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='exampleuser@example.com',
            password='123password',
        )

    def test_list_users(self):
        """Test listed users"""
        url = reverse('admin:user_user_changelist')
        response = self.client.get(url)
        self.assertContains(response, self.user.email)

    def test_page_edit_user(self):
        """Test the edit user page"""
        url = reverse('admin:user_user_change', args=[self.admin_user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_page_create_user(self):
        """Test create user admin page"""
        url = reverse('admin:user_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
