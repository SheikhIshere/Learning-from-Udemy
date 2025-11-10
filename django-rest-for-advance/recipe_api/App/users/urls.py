"""url mapping for the user api"""
from django.urls import path
from .views import CreateUserVIew

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserVIew.as_view(), name='create')
]