"""views for the recipe api"""


# for test
from rest_framework.parsers import MultiPartParser, FormParser


from rest_framework import (
    viewsets, 
    mixins,
    status
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (
    RecipeSerializer,
    RecipeDetailsSerializer,
    TagSerialization,
    IngredientSerializer,
    RecipeImageSerializer
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
        """retrieving recipe for authenticated user"""
        return self.queryset.filter(user = self.request.user).order_by('-id')

    def get_serializer_class(self):
        """return serializers class for request"""
        if self.action == 'list':
            return RecipeSerializer

        # elif self.action == 'upload-image': 
        #fixed instead of sending to desired url i am enter wrong url 
        elif self.action == 'upload_image':
            return RecipeImageSerializer

        
        return self.serializer_class

    def perform_create(self, serializer):
        """creating new recipe"""
        serializer.save(user = self.request.user)

    # @action(methods=['POST'], detail=True, url_path='upload-image')
    # def upload_image(self, request, pk=None):
    #     """upload an image to recipe"""
    #     recipe = self.get_object()
    #     serializer = self.get_serializer(recipe, data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # added this in order to fix bug
    # @action(methods=['POST'], detail=True, url_path='upload-image')
    @action(methods=['POST'], detail=True, url_path='upload-image', parser_classes=[MultiPartParser, FormParser])
    def upload_image(self, request, pk=None):
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseRecipeAttrViewSet(
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin, 
        mixins.ListModelMixin, 
        viewsets.GenericViewSet
    ):
    """this is a base class to support tag and  ingredient as part of refactoring process """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """filter query set for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')




class TagViewSet(BaseRecipeAttrViewSet):
    """manage tags in the data base"""
    serializer_class = TagSerialization
    queryset = Tag.objects.all()

    

class IngredientViewset(BaseRecipeAttrViewSet):
    """here i am managing ingredient in the data base"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
