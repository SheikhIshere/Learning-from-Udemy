"""test for the models like recipe + etc"""

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from django.test import TestCase
from recipe.models import (
    Recipe,
)
from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailsSerializer,
)

from django.contrib.auth import get_user_model

User = get_user_model()

RECIPE_URLS = reverse('recipe:recipe-list')

def create_recipe(user, **params):
    """create and return simple recipe"""
    default = {
        'title': 'simple recipe',
        'description': 'example discription',
        'time_minuts': 22,
        'price': Decimal('5.25'),
        'link': 'http://example.com//recipe.pdf'
    }

    default.update(params)
    recipe = Recipe.objects.create(user = user, **default)
    return recipe


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


class PublicRecipeApiTest(TestCase):
    """testing for the unauthenticated api request"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_require(self):
        """Test: auth is require to call api"""
        res = self.client.get(RECIPE_URLS)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivetRecipeApiTest(TestCase):
    """Tast: authenticate recipe api call"""

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            'test@example.com',            
            'testpass123',
        )
        self.client.force_authenticate(self.user)
    
    def test_retrive_recipe(self):
        """Test: retriving list of recipe"""
        create_recipe(user= self.user)
        create_recipe(user= self.user)

        res = self.client.get(RECIPE_URLS)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many = True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_recipe_list_limited_to_user(self):
        """Test list of recipe is limited to authenticated user"""
        other_user = User.objects.create_user(
            'otheruser@example.com',
            'otheruserpass123'
        )
        create_recipe(user = other_user)
        create_recipe(user = self.user)

        res = self.client.get(RECIPE_URLS)

        recipes = Recipe.objects.filter(user = self.user)
        serializer = RecipeSerializer(recipes, many = True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)