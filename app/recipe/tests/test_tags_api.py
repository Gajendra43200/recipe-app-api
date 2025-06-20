# Test for tags api 
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import (
    Tag,
    Recipe,
)
from decimal import Decimal

from recipe.serializers import (
    TagSerializer, # vid-92-96 s14
)

TAG_URL = reverse('recipe:tag-list')

def detail_url(tag_id):
    # Create and return a tag detail_url
    return reverse('recipe:tag-detail', args=[tag_id])


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

    def test_update_tag(self):
        # Test updating tag 
        tag = Tag.objects.create(user=self.user, name='After dinner')
        payload = {'name': 'Dessert'}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])
    
    def test_delete_tag(self):
        # Test deleting a tag.
        tag = Tag.objects.create(user=self.user, name='Breakfast')
        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags =  Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())
    
    def test_filter_tags_assigned_to_recipes(self):
        # test listing tags to those assigned to recipes
        tag1 = Tag.objects.create(user=self.user, name='Breskfast')
        tag2 = Tag.objects.create(user=self.user, name='Lunch')
        recipe = Recipe.objects.create(
            title=' apple crumble',
            time_minutes=5,
            price=Decimal('4.50'),
            user = self.user,
        )
        recipe.tags.add(tag1)

        res = self.client.get(TAG_URL, {'assigned_only': 1})

        s1 = TagSerializer(tag1)
        s2 = TagSerializer(tag2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)
    
    def test_filtered_tags_unique(self):
        #  test filtered tax returns, a unique list
        tag = Tag.objects.create(user=self.user, name='Breskfast')
        Tag.objects.create(user=self.user, name='Dinner')
        recipe1 = Recipe.objects.create(
            title='Pancakes',
            time_minutes=5,
            price=Decimal('4.50'),
            user = self.user,
        )
        recipe2 = Recipe.objects.create(
            title='Porridge',
            time_minutes=5,
            price=Decimal('2.50'),
            user = self.user,
        )
        recipe1.tags.add(tag)
        recipe2.tags.add(tag)
        res = self.client.get(TAG_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)



