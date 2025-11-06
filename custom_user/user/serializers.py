from rest_framework import (
    serializers,
    status,
)
from .models import UserProfile


class HelloSerializer(serializers.Serializer):
    """ Serializer is a name field to testing our serializers """
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """it will be serializing the user profile"""
    class Meta:
        model = UserProfile
        fields = (
            'id',
            'email',
            'name',
            'password',
        )
        extra_kwargs = {
            'password':{
                'write_only': True
            },
            'style':{
                'input_type': 'password'
            }
        }
    
    def create(self, validated_data):
        """this is for create new user"""
        user = UserProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        
        return super().update(instance, validated_data)