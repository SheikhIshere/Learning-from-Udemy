"""views for the recipe api"""


# for test (passed)
from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import(
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
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
#         """retrieving recipe for authenticated user"""
#         return self.queryset.filter(user = self.request.user).order_by('-id')


"""
this is kinda advance one ,this one not only show list but also shows details
"""  
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,  # ← add this
                description = 'comma separated list of ids to filter',
            ),
            OpenApiParameter(
                'ingredient',
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,  # ← add this
                description = 'comma separated list of ids to filter',     
            )
        ]
    )
)  
class RecipeViewset(viewsets.ModelViewSet):
    """view for manage recipe api"""
    serializer_class = RecipeDetailsSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )


    def _params_to_ints(self, qs):
        """convert list of string to ing"""
        return[int(str_id) for str_id in qs.split(',')]
    
    def get_queryset(self):
        """retrieving recipe for authenticated user"""
        # return self.queryset.filter(user = self.request.user).order_by('-id')
        tags = self.request.query_params.get('tags')
        ingredient = self.request.query_params.get('ingredient')
        queryset = self.queryset

        if tags:
            tags_id = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tags_id)
        
        if ingredient:
            ingredient_id = self._params_to_ints(ingredient)
            # queryset = queryset(ingredient__id__in=ingredient_id) # bug didn't added filter
            queryset = queryset.filter(ingredient__id__in=ingredient_id) # fixed
        
        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()


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



@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description = 'Filter by items assigned to recipes',
            )
        ]
    )
)  
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
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)
        # return self.queryset.filter(user=self.request.user).order_by('-name')
        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()




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
