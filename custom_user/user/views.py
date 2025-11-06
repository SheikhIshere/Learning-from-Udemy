from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from .serializers import (
    HelloSerializer, 
    UserProfileSerializer
)
from .models import(
    UserProfile
)
from rest_framework import viewsets
from .permissions import UpdateOwnProfile
from rest_framework import filters

class HelloApi(APIView):
    """this is just for testing the api view"""
    serializer_class = HelloSerializer
    def get(self, request, format = None):
        """return a list of api view features"""
        feature_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'is similer with a traditional django view',
            'gives you the most control over you application logic',
            'is mapped manually to URLs',
        ]

        return Response(
            {
                'message': 'Hello!',
                'an_apiview': feature_apiview
            },
            status = 200
        )

    def post(self, request):
        """creating hello with a custom name"""
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            messege = f'hello {name}'
            return Response(
                {
                    'message': messege
                },
                status = 200
            )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )


    def put(self, request, pk = None):
        """handel updating an object"""
        return Response(
            {
                'method': 'PUT'
            }
        )
    
    def patch(self, request, pk = None):
        """handel updating part of an object"""
        return Response(
            {
                'method': 'PATCH'
            }
        )
    
    def delete(self, request, pk = None):
        """"Deleting the object"""
        return Response(
            {
                'method': 'DELETE'
            }
        )


class HelloViewSet(viewsets.ViewSet):
    """testing api viewset"""
    serializer_class = HelloSerializer
    def list(self, request):
        """return a hello message"""
        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]
        return Response(
            {
                'messege': 'hello',
                'a_viewset': a_viewset
            }
        )
    
    def create(self, request):
        """creating a new hello messege"""
        serializer = self.serializer_class(data = request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            messege = f"hello {name}"
            return Response(
                {
                    'messege': messege,
                }
            )
        else:
            return Response(                
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST                
            )
    
    def retrieve(self, request, pk = None):
        """handeling an object by it's id"""
        return Response(
            {
                'http method': 'GET'
            }
        )
    
    def update(self, request, pk = None):
        """handeling updating an object"""
        return Response(
            {
                "http method": 'PUT'
            }
        )
    
    def partial_update(self, request, pk = None):
        """handeling updating part of an object"""
        return Response(
            {
                'http method': 'PATCH'
            }
        )

    def destroy(self, request, pk = None):
        """handeling the deletation of any object"""
        return  Response(
            {
                'http response': 'DELETE'
            }
        )


class UserProfileViewSet(viewsets.ModelViewSet):
    """handeling the user create and update of profiel"""
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email', )
