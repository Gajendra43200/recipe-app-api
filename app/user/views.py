# Views for user apis 
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

class CreateUserView(generics.CreateAPIView):
    # How does a lot of the logic that we need for creating objects in the database for us?
    # create a new  user in the system 
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    # Create  a new auth token for user 
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    # Manage authenticate user 
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication] 
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Retrive and return the authenticate user 
        return self.request.user
