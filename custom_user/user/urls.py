from django.urls import path, include
from .views import (
    HelloApi,
    HelloViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hello-viewset', HelloViewSet, basename='hello-viewset')




urlpatterns = [
    path('hello-view/', HelloApi.as_view()),
    path('', include(router.urls))
]