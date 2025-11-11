"""serializers for recipe api app"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Recipe

User = get_user_model()


class RecipeSerializer(serializers.ModelSerializer):
    """Serializers for recipes"""
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'time_minuts', 'price', 'link']
        read_only_fields = ['id']