from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
# Create your models here.
from django.contrib.auth import get_user_model
from django.conf import settings

class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """ create a new user profile """
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """ create and save a new superuser with given details """
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    ''' database model for user system '''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """ retrive full name of user """
        return self.name

    def get_short_name(self):
        """ retrive short name of user """
        return self.name
    
    def __str__(self):
        """ return string representation of our user """
        return self.email


User = get_user_model()


class ProfileFeed(models.Model):
    """profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.status_text