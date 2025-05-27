# Views for user apis 
from rest_framework import generics
from user.serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    # How does a lot of the logic that we need for creating objects in the database for us?
    # create a new  user in the system 
    serializer_class = UserSerializer