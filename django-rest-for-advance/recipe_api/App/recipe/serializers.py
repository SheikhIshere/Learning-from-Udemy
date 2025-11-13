"""serializers for recipe api app"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Recipe,
    Tag,
)

User = get_user_model()


class TagSerialization(serializers.ModelSerializer):
    """serializer for tag"""
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_field = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializers for recipes"""
    tags = TagSerialization(many = True, required = False)
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minuts', 'price', 'link', 'tags']
        read_only_fields = ['id']

    # it's a helper fuction to support create and update for dry
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
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context['request'].user
        
        self._get_create_tags(tags=tags, recipe=recipe)

        return recipe

    def update(self, instance, validated_data):
        """Updating recipe"""
        tags = validated_data.pop('tags', None)

        if tags is not None:
            instance.tags.clear()
            self._get_create_tags(tags, instance)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance




class RecipeDetailsSerializer(RecipeSerializer):
    """serializer for recipe detail view"""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']


