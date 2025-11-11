"""views for the recipe api"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import RecipeSerializer
from .models import Recipe


class RecipeViewset(viewsets.ModelViewSet):
    """view for manage recipe api"""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """retriving recipe for authhnticated user"""
        return self.queryset.filter(user = self.request.user).order_by('-id')