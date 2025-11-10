"""
serializers.py for user api
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializers(serializers.ModelSerializer):
    """serializers for user serializers"""
    password = serializers.CharField(
        write_only=True,
        min_length=5,
        style={'input_type': 'password'}
    )
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        # extra_kwargs = {'password': {'write_only': True}, 'min_length': 5}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
