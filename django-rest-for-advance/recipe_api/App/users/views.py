"""views for the useer api"""

from rest_framework import generics
from .serializers import UserSerializers


class CreateUserVIew(generics.CreateAPIView):
    """creating new user in the system"""
    serializer_class = UserSerializers
