# Database models 
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


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