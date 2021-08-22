from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import permissions, serializers
from profiles_api import models

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

    def put(self,request, pk=None):

        return Response({'method':'PUT'})

    def patch(self,request, pk=None):

        return Response({'method':'PATCH'})
    
    def delete(self,request, pk=None):

        return Response({'method':'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentications tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated
    )

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)