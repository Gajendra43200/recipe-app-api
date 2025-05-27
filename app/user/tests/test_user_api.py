from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


# Public is basically unauthenticated requests, so requests that don't require authentication.
class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_success(self):
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        # So that's the URL for the create user API and will pass in the payload
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        # And what this line does is it retrieves the object from the database with the email address that we
        # passed in as the payload.vid-67-70
        self.assertTrue(user.check_password(payload['password']))
        # we gave in the payload in order to check that this asset's true, which means that the password is correct.
        self.assertNotIn('password', res.data)

    def test_user_with_email_exits_error(self):
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short_error(self):
        # An error is returned if password less than five chars or five characters.
        payload = {
            'email': 'test@example.com',
            'password': 't23',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists= get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)


