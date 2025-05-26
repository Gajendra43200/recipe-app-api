# Test for the django admin modifications vid 55 section 10
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123'
        )
        self.client.force_login(self.admin_user)
        # And then we call this force logging method here which allows us to force the authentication to this user.

        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )
    
    def test_user_list(self):
        # Test that user list on page
        url = reverse('admin:core_user_changelist') # And what we're going to do is use reverse to get the URL for the change list inside the Django app.
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
    
    def test_edit_user_page(self):
        # Test the edit user page work vid 57-60
        url = reverse('admin:core_user_change', args=[self.user.id]) #And this is the URL for the change user page and we need 
        # to pass in a specific ID for the user that we want to change.
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
    
    def test_ctreate_user_page(self):
        # Test the create suer page work
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)