"""test for the models like recipe + etc"""
from decimal import Decimal
from django.test import TestCase
from recipe.models import (
    Recipe,

)
from django.contrib.auth import get_user_model


User = get_user_model()


class RecipeTesting(TestCase):
    """testing recipe"""

    def test_create_recipe(self):
        """testing creating recipe is successfull"""
        user = User.objects.create_user(
            'test@example.com',
            'testpass123',
        )
        recipe = Recipe.objects.create(
            user = user,
            title = 'example recipe name',
            description = 'Sample of recipe',
            time_minuts = 5,
            price = Decimal('5.50'),
            link = 'none', # don't think this is causing problem
        )

        self.assertEqual(str(recipe), recipe.title)