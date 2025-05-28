# Views for recipe api 
from rest_framework import(
    viewsets,
    mixins,
    # Mix ins is just things that you can mix in to a view to add additional functionality.
)
# from rest_framework import viewsets, permissions

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import(
    Recipe,
    Tag,
)
from recipe import serializers
# from recipe.serializers import RecipeSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    # view set it specifically set up to work directly with a model.
    # view for manage recipe apis. 
    serializer_class = serializers.RecipeDetailsSerializer
    queryset = Recipe.objects.all()
    # permission_classes = [IsAuthenticated]

    # So the query SAT represents the objects that were available for this view.
    # So because it's a model view set is expected to work with a model.
    authentication_calsses = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrive recipes for authenticated user 
        return self.queryset.filter(user=self.request.user).order_by('-id')
    
    def get_serializer_class(self):
        # Return the serializer class for request.
        if self.action == 'list':
            return serializers.RecipeSerializer
        
        return self.serializer_class
    
    def perform_create(self, serializer):
        # Create a new recipe. 
        serializer.save(user=self.request.user)

class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    # Manage tesg in the datasets
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter query set to authenticate user
        return self.queryset.filter(user=self.request.user).order_by('-name')
    