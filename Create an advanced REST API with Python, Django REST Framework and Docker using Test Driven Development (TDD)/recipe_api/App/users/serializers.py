"""
serializers.py for user api
"""

from rest_framework import serializers
from django.contrib.auth import (
    get_user_model,
    authenticate
)
from django.utils.translation import gettext_lazy as _

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
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
            
        return user

class AuthTokenSerializer(serializers.Serializer):
    """serializers for auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request = self.context.get('request'),
            username = email,
            password = password
        )
        if not user:
            msg = _('Unable to authenticate using the provided credentials.')
            raise serializers.ValidationError(msg, code = 'authorization')
        
        attrs['user'] = user
        return attrs