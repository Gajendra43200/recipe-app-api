# Database models 
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.conf import settings 



class UserManager(BaseUserManager):
    # Manager for user 
    def create_user(self, email, password=None, **extra_fields):
        # Create save and return a new user 
        if not email:
            raise ValueError('User must have email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
        # edit settings.py file
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length= 256, unique=True)
    name = models.CharField(max_length=233)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    # So if staff is used to determine if the user can log into the Django admin, so only staff users can log in.
    # And by default we don't want regular users to be able to log into the unknown.
    # So we set it to false.
    objects = UserManager()
    USERNAME_FIELD = 'email'
    # Then we have the username field here which defines the field that we want to use for authentication.

class Recipe(models.Model):
    # 'Recipe object.vid:79-84'
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        # we delete that user object from the system, it's also going to delete all the recipes
        # that are associated to the user.
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    # Then we have a link which can be used to store a link to the recipe if there's some external link or
    # something that you want to link out to.
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    # So we use the many to many field because we could have many different recipes that have many differentn
    # tags.

    def __str__(self):
        # the string representation of that object.
        # So if you have an object of the recipe and 
        # you print it out as a string, then this is what will be returned.
        return self.title
    
class Tag(models.Model):
    # Tag for filtering recipe vid:91-96 -s 14
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=225)
    user  = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return self.name
