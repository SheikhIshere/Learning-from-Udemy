"""here is the recepe admin panel where i will be register the admin staffs to see it"""

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Recipe, Tag, Ingredient

@admin.register(Recipe)
class RecipeAdminModel(ModelAdmin):
    list_display = [
        'user',
        'title',
        'time_minutes',
        'price',
    ]

@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = [
        'user',
        'name',
    ]


@admin.register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = [
        'user',
        'name'
    ]