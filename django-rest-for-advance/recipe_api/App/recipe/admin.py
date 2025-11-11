"""here is the recepe admin panel where i will be register the admin staffs to see it"""

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdminModel(ModelAdmin):
    list_display = [
        'user',
        'title',
        'time_minuts',
        'price',
    ]
