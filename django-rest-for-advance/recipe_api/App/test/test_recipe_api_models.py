"""test for the models like recipe + etc"""

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from django.test import TestCase
from recipe.models import (
    Recipe,
    Tag,
)
from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailsSerializer,
    TagSerialization,
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

def details_urls(recipe_id):
    """creating and returninng recipe urls"""
    return reverse('recipe:recipe-detail', args=[recipe_id])

def create_user(**params):
    """create_and_return_new_user"""
    return User.objects.create_user(
        **params
    )


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
            link = 'none',
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

        # i am removing this cz i have created helper function to do that
        # self.user = User.objects.create_user(
        #     'test@example.com',            
        #     'testpass123',
        # )

        # helper function related user creation
        self.user = create_user(email='test2@example.com', password='testpass123')
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
        # removing this cz i am using helper function
        # other_user = User.objects.create_user(
        #     'otheruser@example.com',
        #     'otheruserpass123'
        # )
        other_user = create_user(email='otheruser@example.com', password='otheruserpass123')
        create_recipe(user = other_user)
        create_recipe(user = self.user)

        res = self.client.get(RECIPE_URLS)

        recipes = Recipe.objects.filter(user = self.user)
        serializer = RecipeSerializer(recipes, many = True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """test get recipe detail"""
        recipe = create_recipe(user = self.user)

        url = details_urls(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailsSerializer(recipe)

        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """test creating recipe"""
        payload = {
            'title': 'Cat comb meat dish',
            'description': 'delicious cat food, yum!!',
            'time_minuts': 30,
            'price': Decimal('3.99'),
            'link': 'https://www.youtube.com/shorts/dko1j1V0HsI',
        }
        res = self.client.post(RECIPE_URLS, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])

        for k,v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        
        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        """Test partial update for recipe"""
        original_link = 'https://example.com/recipe.pdf'
        recipe = create_recipe(
            user=self.user,
            title = 'test title',
            link = original_link,
        )
        payload = {'title':'new recipe title'}
        url = details_urls(recipe_id=recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)
    
    def test_full_update(self):
        """test full update of recipe"""
        recipe = create_recipe(
            user=self.user,
            title = 'new recipe title',
            description = 'new recipe description',
            link = 'https://example.com/recipe.pdf',
        )
        payload = {
            'title': 'Cat comb meat dish',
            'description': 'delicious cat food, yum!!',
            'time_minuts': 30,
            'price': Decimal('3.99'),
            'link': 'https://www.youtube.com/shorts/dko1j1V0HsI',
        }

        url = details_urls(recipe_id=recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()

        for k,v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)
    
    def test_update_user_return_error(self):
        """test changing the recipe user results in the error"""
        # new_user =  create_user(email='test2@example.com', password='testpass123')
        new_user = create_user(email='otheruser@example.com', password='testpass123')
        recipe = create_recipe(user=self.user)
        payload = {'user':new_user.id}
        url = details_urls(recipe_id=recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)
    
    def test_delete_recipe(self):
        """test deleteing a recipe successfully"""
        recipe = create_recipe(user=self.user)

        url = details_urls(recipe_id=recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())
    
    def test_recipe_other_users_recipe_error(self):
        """test: trying to delet other user's recipe"""
        new_user = create_user(
            email = 'new3@example.com',
            password = 'password123'
        )
        recipe = create_recipe(user=new_user)

        url = details_urls(recipe_id=recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())

    def test_create_recipe_with_new_tags(self):
        """ test: creating recipe with new tags """
        payload = {
            'title': 'thai prawn curry',
            'time_minuts': 30,
            'price': Decimal('30.99'),
            # finally found the problemm; this have a syntex error
            # 'tags': {
            #     'name': 'thai',
            #     'name': 'dinner',
            # }
            'tags': [
                {'name': 'thai'},
                {'name': 'dinner'},
            ]
        }

        res = self.client.post(RECIPE_URLS, payload, format='json')

        # so this is causing the getting failled , referaring = 400(bad request)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        
        
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 2)

        for tag in payload['tags']:
            exists = recipe.tags.filter(
                name = tag['name'],
                user = self.user,
            ).exists()
            self.assertTrue(exists)
    
    def test_create_recipe_with_existing_tag(self):
        """Test: creating same tag to raise error if exists"""
        tag_indian = Tag.objects.create(user=self.user, name='indian')
        payload = {
            'title': 'dosa',
            'time_minuts':20,
            'price': Decimal('1.50'),
            'tags':[
                {'name': 'indian'},
                {'name': 'south-indian'},
                {'name': 'breakfast'},
            ]
        }

        res = self.client.post(RECIPE_URLS, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 3)
        self.assertIn(tag_indian, recipe.tags.all())

        for tag in payload['tags']:
            exists = recipe.tags.filter(
                name = tag['name'],
                user = self.user
            ).exists()
            self.assertTrue(exists)
    
    def test_create_tags_on_update(self):
        """Test: creating tags when updating recipe"""
        recipe = create_recipe(user=self.user)
        payload = {
            'tags': [
                {'name': 'lunch'}
            ]
        }
        url = details_urls(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        new_tag = Tag.objects.get(user=self.user, name='lunch')
        self.assertIn(new_tag, recipe.tags.all())
    
    def test_update_assign_tag(self):
        """test: assigning a tags existing tags while updating"""
        tag_breakfast = Tag.objects.create(user=self.user, name='breakfast')
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag_breakfast)

        tag_lunch = Tag.objects.create(user=self.user, name='lunch')
        payload = {'tags': [{'name': 'lunch'}]}
        url = details_urls(recipe_id=recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(tag_lunch, recipe.tags.all())
        self.assertNotIn(tag_breakfast, recipe.tags.all())
    
    def test_clear_recipe_tags(self):
        """Test: clearing recipe's tags"""
        tag = Tag.objects.create(user=self.user, name='Dessart')
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag)
        payload = {
            'tags':[]
        }
        url = details_urls(recipe_id=recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tags.count(), 0)