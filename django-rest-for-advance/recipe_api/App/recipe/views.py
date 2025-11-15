"""views for the recipe api"""

from rest_framework import (
    viewsets, 
    mixins
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    RecipeSerializer,
    RecipeDetailsSerializer,
    TagSerialization,
    IngredientSerializer
)
from .models import (
    Recipe,
    Tag,
    Ingredient
)

"""this was made to just show the list"""
# class RecipeViewset(viewsets.ModelViewSet):
#     """view for manage recipe api"""
#     serializer_class = RecipeSerializer
#     queryset = Recipe.objects.all()
#     authentication_classes = (TokenAuthentication, )
#     permission_classes = (IsAuthenticated, )

#     def get_queryset(self):
#         """retriving recipe for authhnticated user"""
#         return self.queryset.filter(user = self.request.user).order_by('-id')


"""
this is kinda advance one ,this one not only show list but also shows details
"""    
class RecipeViewset(viewsets.ModelViewSet):
    """view for manage recipe api"""
    serializer_class = RecipeDetailsSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """retriving recipe for authhnticated user"""
        return self.queryset.filter(user = self.request.user).order_by('-id')

    def get_serializer_class(self):
        """return serializers class for request"""
        if self.action == 'list':
            return RecipeSerializer
        
        return self.serializer_class

    def perform_create(self, serializer):
        """creating new recipe"""
        serializer.save(user = self.request.user)


class TagViewSet(
                mixins.DestroyModelMixin,
                mixins.UpdateModelMixin, 
                mixins.ListModelMixin, 
                viewsets.GenericViewSet):
    
    """manage tags in the data base"""

    serializer_class = TagSerialization
    queryset = Tag.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """filter query set for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
    

class IngredientViewset(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin, 
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    """here i am managing ingredient in the data base"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """filter queryset to authenticated user"""
        return self.queryset.filter(user = self.request.user).order_by('-name')
    