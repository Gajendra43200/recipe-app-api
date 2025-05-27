# Views for recipe api 
from rest_framework import viewsets
# from rest_framework import viewsets, permissions

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Recipe
# from recipe import serializers
from recipe.serializers import RecipeSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    # view set it specifically set up to work directly with a model.
    # view for manage recipe apis. 
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]

    # So the query SAT represents the objects that were available for this view.
    # So because it's a model view set is expected to work with a model.
    authentication_calsses = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrive recipes for authenticated user 
        return self.queryset.filter(user=self.request.user).order_by('-id')
        
    