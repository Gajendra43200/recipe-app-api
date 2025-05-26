#   Test for model
from django.test import TestCase
from django.contrib.auth import get_user_model


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
