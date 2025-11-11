"""creating models for recepi app"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Recipe(models.Model):
    """model for core recipe + objects"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # title = models.CharField(max_length=255), # bug fixed: ','
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minuts = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title