# Views for recipe api 
from rest_framework import(
    viewsets,
    mixins,
    status,
    # Mix ins is just things that you can mix in to a view to add additional functionality.
)
# from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import(
    Recipe,
    Tag,
    Ingredient,
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
        
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        
        return self.serializer_class
    
    def perform_create(self, serializer):
        # Create a new recipe. 
        serializer.save(user=self.request.user)
    
    @action(methods=['POST'], detail=True, url_path='upload_image')
    def upload_image(self, request, pk=None):
        # Upload image to recipe.
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
        viewsets.GenericViewSet,
    ):
    # Base viewsets for recipe attributes
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter query set to authenticate user
        return self.queryset.filter(user=self.request.user).order_by('-name')

    

class TagViewSet(BaseRecipeAttrViewSet):
    # Manage tesg in the datasets
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     # Filter query set to authenticate user
    #     return self.queryset.filter(user=self.request.user).order_by('-name')
    
class IngredientViewSet(BaseRecipeAttrViewSet):
    # Manage ingredient in the data set
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     # Filter query set for unthenticated user
    #     return self.queryset.filter(user=self.request.user).order_by('-name')
    