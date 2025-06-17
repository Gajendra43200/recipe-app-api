#   Test for model
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models
from unittest.mock import patch

def create_user(email = "user@example.com", password =  'testpass123'):
    # Create and return new user vid-91-96 s-14 
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    # Test model 
    def test_create_user_with_email_successful(self):
        email = "test@example.com"
        password =  'testpass123'
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        # self.assertEqual(user.check_password(password),  password)
        # check_password = And in order to do that, we need to use the check 
        # password method that is provided by the default model

    def test_new_user_email_nomalized(self):
        sample_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.com', 'test4@example.com']
        ]

        for email, excepted in sample_email:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, excepted)
    

    def test_new_user_without_email_raise_error(self):
        # create user method raises an exception if we provide an empty user.
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    
    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    
    def test_create_recipe(self):
        # Tesst creating recipe successfuly vid 78-83
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        # And the reason we're creating a user is because we're going to use this user to assign to our recipe
        # objects.
        recipe = models.Recipe.objects.create(
            user=user,
            title='Simple recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Simple recipe description.',
        )
        
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        # Creating a tag is seuccess vid-91-96 s-14 
        user = create_user()
        tag = models.Tag.objects.create(user= user, name='Tag1')
        self.assertEqual(str(tag), tag.name)
        # Then we are checking when we convert this tag instance to a string using the str built in function
    # vid 106-112 section 15
    def test_create_ingredient(self):
        # Test creating ingredient sucessful
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user = user,
            name = 'Ingredient1'
        )
        self.assertEqual(str(ingredient), ingredient.name)
    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        # Test generating image path
        uuid = 'test_uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')
        