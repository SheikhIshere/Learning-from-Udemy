"""url mapping for recipe app"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RecipeViewset,
    TagViewSet
)


router = DefaultRouter()
router.register('recipe', RecipeViewset)
router.register('tags', TagViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]