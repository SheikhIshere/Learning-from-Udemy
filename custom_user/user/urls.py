from django.urls import path, include
from .views import (
    HelloApi,
    HelloViewSet,
    UserProfileViewSet,
    UserLoginApiView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hello-viewset', HelloViewSet, basename='hello-viewset')
router.register('profile', UserProfileViewSet, basename='user_profile')



urlpatterns = [
    path('hello-view/', HelloApi.as_view()),
    path('login/', UserLoginApiView.as_view()),
    path('', include(router.urls))
]