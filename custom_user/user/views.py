from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class HelloApi(APIView):
    """this is just for testing the api view"""

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