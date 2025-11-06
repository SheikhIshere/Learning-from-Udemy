from django.urls import path, include
from .views import HelloApi




urlpatterns = [
    path('hello-view/', HelloApi.as_view()),
]