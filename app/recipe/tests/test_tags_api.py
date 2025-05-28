# Test for tags api 
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag

from recipe.serializers import (
    TagSerializer, # vid-92-96 s14
)

TAG_URL = reverse('recipe:tag-list')

def create_user(email='user@example.com', password='testpass123'):
    return get_user_model().objects.create_user(email=email, password=password)

class PublicTagsApiTests(TestCase):
    # Test unuthonticated api request
    
    def setUp(self):
        self.client = APIClient()
    
    def test_auth_required(self):
        # Test auth is required for the retreving tags 
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTests(TestCase):
    # Test authontication is required 
    
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        # Test retrieveing tag list of the Tag
        Tag.objects.create(user=self.user, name="Gajendra")
        Tag.objects.create(user=self.user, name="Prince")

        res = self.client.get(TAG_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        # just one object, it's going to be multiple objects.
        # So it will be a list of objects.
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_tags_limited_to_user(self):
        # Test list of tags is limited to authenticated user.
        user2= create_user(email='user2@example.com', )
        Tag.objects.create(user=user2, name='prince12')
        tag = Tag.objects.create(user=self.user, name='Comford food')
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)
        

