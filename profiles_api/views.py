from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from profiles_api import serializers


class HelloApiView(APIView):
    """Test api view"""
    serializer_class = serializers.HelloSerializer


    def get(self, request, format=None):
        """Returns a list of api features"""
        an_apiview = [
            'Uses https methods as functions (get,post,patch,put,delete)',
            'is similar to a tradiciona django View',
            'Gives you the most control over you application logic',
            'is mapped manually to URLS'

        ]

        return Response({'message':'Hello','an_apiview':an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
             )