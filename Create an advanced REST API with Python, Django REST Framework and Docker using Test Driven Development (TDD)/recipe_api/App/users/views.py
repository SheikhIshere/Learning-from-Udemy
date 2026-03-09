"""views for the useer api"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import (
    UserSerializers,
    AuthTokenSerializer
)


class CreateUserVIew(generics.CreateAPIView):
    """creating new user in the system"""
    serializer_class = UserSerializers


class CreateTokenView(ObtainAuthToken):
    """new auth token for auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# class ManageUserView(generics.RetrieveAPIView):
class ManageUserView(generics.RetrieveUpdateAPIView):
    """manage the authenticated user"""
    serializer_class = UserSerializers
    # authentication_class = (authentication.TokenAuthentication,) # didn't used es
    authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = [permissions.IsAuthenticated] 
    permission_classes = (permissions.IsAuthenticated, ) # plural must fixed

    def get_object(self):
        """retrive and return authenticated user"""
        return self.request.user