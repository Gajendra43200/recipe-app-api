# Test for recipes api. 
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import(
    Recipe,
    Tag,
)
from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailsSerializer, #vid:83-88
)

RECIPES_URL = reverse('recipe:recipe-list')

def details_url(recipe_id):
    # Create and return a recipe details_url
    return reverse('recipe:recipe-detail', args=[recipe_id])

def create_recipe(user, **params):
    # create and return simple recipe 
    defaults = {
        'title': 'Simple recipe title',
        'time_minutes': 22,
        'price': Decimal('5.30'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf',
    }

    defaults.update(params)
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicRecipeAPITests(TestCase):
    # Test unauthenticated api requests 

    def setUp(self):
        self.client = APIClient()
    
    def test_auth_required(self):
        # Test auth to required api call. 
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTests(TestCase):
    # Test authenticated api requested 

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.user = get_user_model().objects.create_user(
            'user1@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)
    
    def test_retrive_recipe(self):
        # Test retriving list of Recipe
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True) # And when you pass in many equals, true tells it that we want to pass in a list of items.
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_recipe_list_limited_to_user(self):
        # Test list of Recipes limited to authenticated user
        other_user = create_user(
            email = 'other@example.com',
            password = 'testpass123',
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_datail(self):
        # Test get Recipe detail 
        recipe = create_recipe(user=self.user)
        url = details_url(recipe.id)
        serializer = RecipeDetailsSerializer(recipe)
        self.assertEqual(serializer.data, serializer.data)

    def test_create_recipe(self):
        # Test ctreating recipe vid:85-90
        payload = {
            'title': 'Simple recipe',
            'time_minutes': 30,
            'price': Decimal('5.99'),
        }

        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        # Test partial update Recipe 
        original_link = 'http://example.com/recipe.pdf'
        recipe = create_recipe(
            user=self.user,
            title='Simple recipe title',
            link=original_link,
        )

        payload = {'title': 'New recipe title'}
        url = details_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)

    def full_update(self):
        recipe = create_recipe(
            user=self.user,
            title='Simple recipe title',
            link='http://example.com/recipe.pdf',
            description="simple recipe description for the recipe",
        )

        payload = {
            'title': 'new Sample recipe',
            'time_minutes': 10,
            'link': 'http://example.com/recipe.pdf',
            'price': Decimal('5.99'),
            'description': "new simple recipe description for the recipe",
        }
        url = details_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_update_user_returns_error(self):
        new_user = create_user(email='user2@example.com', password='test123')
        recipe = create_recipe(user=self.user)

        paylaod = {'user': new_user.id}
        url = details_url(recipe.id)
        self.client.patch(url, paylaod)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)
    
    def test_delete_recipe(self):
        recipe = create_recipe(user=self.user)
        url = details_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())
    
    def test_delete_other_users_recipe_error(self):
        new_user = create_user(email='user2@example.com', password='test123')
        recipe = create_recipe(user=new_user)
        url = details_url(recipe.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())

    def test_create_recipe_with_new_tag(self):
        # Test creating Recipe with new tags VID:99-104
        payload = {
            'title': 'this is new recipe',
            'time_minutes': 30,
            'price': Decimal('2.45'),
            'tags': [{'name': 'Thai'}, {'name': 'Dinner'}],
        }
        res = self.client.post(RECIPES_URL, payload, format='json')
        # And because we're providing nested objects here, we want to set format equals Jason.
        # So just to make sure it gets converted to Jason and is successfully posted to the API.

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        # self.assertEqual(recipe.tags.count(), 2)
        for tag in payload['tags']:
            exists = recipe.tags.filter(
                name=tag['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)
    
    def test_create_recipe_with_existing_tags(self):
        # Create a recipe with existing tags VID:99-104
        tag_indian = Tag.objects.create(user=self.user, name='indian')
        payload = {
            'title': 'new tag',
            'time_minutes': 60,
            'price': Decimal('4.50'),
            'tags': [{'name': 'indian'}, {'name': 'breakfast'}]
        }
        res = self.client.post(RECIPES_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 2)
        self.assertIn(tag_indian, recipe.tags.all())
        for tag in payload['tags']:
            exists = recipe.tags.filter(
                name=tag['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)
   
    def test_create_tag_on_update(self):
        # test crate tag when updating a Recipe
        recipe = create_recipe(user=self.user)
        payload = {'tags': [{'name': 'Lunch'}]}
        url = details_url(recipe.id)
        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_tag = Tag.objects.get(user=self.user, name = 'Lunch')
        self.assertIn(new_tag, recipe.tags.all())
    
    def test_update_recipe_assign_tag(self):
        # test for assigning an existting tag when updating tag.
        tag_breakfast = Tag.objects.create(user=self.user, name = 'Breakfast')
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag_breakfast)

        tag_lunch = Tag.objects.create(user=self.user, name = 'Lunch')
        payload = {'tags': [{'name': 'Lunch'}]}
        url = details_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(tag_lunch, recipe.tags.all())
        self.assertNotIn(tag_breakfast, recipe.tags.all())

    def test_clear_recipe_tags(self):
        tag = Tag.objects.create(user = self.user, name='Dessert')
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag)
        
        payload = {'tags': []}
        url = details_url(recipe.id)
        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tags.count(), 0)







