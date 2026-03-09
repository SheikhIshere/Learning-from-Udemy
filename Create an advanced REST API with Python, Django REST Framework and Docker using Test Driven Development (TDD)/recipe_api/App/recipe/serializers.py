"""serializers for recipe api app"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Recipe,
    Tag,
    Ingredient
)

User = get_user_model()



class IngredientSerializer(serializers.ModelSerializer):
    """serializer for ingredient"""
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class TagSerialization(serializers.ModelSerializer):
    """serializer for tag"""
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializers for recipes"""
    tags = TagSerialization(many = True, required = False)
    ingredient = IngredientSerializer(many = True, required = False)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'time_minutes', 
            'price', 'link', 'tags', 'ingredient'
        ]
        read_only_fields = ['id']

    # it's a helper fuction to support create and update for dry
    def _get_or_create_ingredients(self, ingredient, recipe):
        """handel getting or creating ingredient as needed"""
        auth_user = self.context['request'].user
        for ing in ingredient:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ing,
            )
            recipe.ingredient.add(ingredient_obj)

    def _get_create_tags(self, tags, recipe):
        """handel getting or creating tags as needed"""
        auth_user = self.context['request'].user

        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user = auth_user,
                **tag
            )
            recipe.tags.add(tag_obj)

    def create(self, validated_data):
        """create recipe"""
        tags = validated_data.pop('tags', [])
        ingredient = validated_data.pop('ingredient', [])
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context['request'].user
        
        self._get_create_tags(tags=tags, recipe=recipe)
        self._get_or_create_ingredients(ingredient, recipe)

        return recipe

    def update(self, instance, validated_data):
        """Updating recipe"""
        tags = validated_data.pop('tags', None)
        ingredient = validated_data.pop('ingredient', None)


        if tags is not None:
            instance.tags.clear()
            self._get_create_tags(tags, instance)

        # newly implemented to fix bug
        if ingredient is not None:
            instance.ingredient.clear()
            self._get_or_create_ingredients(ingredient, instance)

        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance




class RecipeDetailsSerializer(RecipeSerializer):
    """serializer for recipe detail view"""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description', 'image']


class RecipeImageSerializer(serializers.ModelSerializer):
    """serializer for uploading images to recipe """
    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        # extra_kwargs = {'image': {'required': 'True'}}
        extra_kwargs = {'image': {'required': True}}
