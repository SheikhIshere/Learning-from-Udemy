from django.db import models

# Create your models here.

class Category(models.Model):
    """this is category model"""
    name = models.CharField(max_length=50)
    is_active = models.BooleanField()
    level = models.SmallIntegerField()

    class Meta:
        db_table = 'category'




class PromotionEven(models.Model):
    """promotion event model"""
    pass


class Product(models.Model):
    """Product model"""
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    