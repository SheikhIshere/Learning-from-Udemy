from rest_framework import (
    serializers,
    status,
)
from .models import (
    UserProfile,
    ProfileFeed
)


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
    

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializers for feed item"""
    class Meta:
        model = ProfileFeed
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {
            'user_profile': {
                'read_only': True
            },
            'created_on': {
                'read_only': True
            }
        }