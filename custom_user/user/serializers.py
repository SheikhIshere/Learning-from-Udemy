from rest_framework import (
    serializers,
    status
)
from .models import UserProfile


class HelloSerializer(serializers.Serializer):
    """ Serializer is a name field to testing our serializers """
    name = serializers.CharField(max_length=10)
