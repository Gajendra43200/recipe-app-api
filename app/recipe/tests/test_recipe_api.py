# Test for recipes api. 
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe
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
        self.user = get_user_model().objects.create_user(
            'user@example.com',
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
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'testpass',
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

