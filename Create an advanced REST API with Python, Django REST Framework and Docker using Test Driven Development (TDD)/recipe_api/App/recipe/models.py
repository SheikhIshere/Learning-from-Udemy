"""creating models for the recipe app"""
import uuid
import os


def recipe_image_file_path(instance, filename):
    """generate file path for new recipe image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)


from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Recipe(models.Model):
    """model for core recipe + objects"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # title = models.CharField(max_length=255), # bug fixed: ','
    title = models.CharField(max_length=255, null=True, blank=True )
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    tags = models.ManyToManyField('Tag')
    ingredient = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """creating tag model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50) # just following instructor - not get extra pain, for now only

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ingredient for recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name