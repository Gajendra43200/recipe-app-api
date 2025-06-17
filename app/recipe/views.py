# Views for recipe api 
from rest_framework import(
    viewsets,
    mixins,
    status,
    # Mix ins is just things that you can mix in to a view to add additional functionality.
)

from drf_spectacular.utils import(
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
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

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of IDs to filter',
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingredients IDs to filter',
            )
        ]
    )
)
# So that should be all we need to do to update the documentation.
# We're using the extend schema view, which is the
# decorator that allows us to extend the auto generated
# schema that's created by Django rest spectacular.
# Then we're defining lists.

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

    def _params_to_ints(self, qs):
        # Convert list of string to integers
        # '1,2,3'
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        # Retrive recipes for authenticated user 
        # return self.queryset.filter(user=self.request.user).order_by('-id')
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        
        if ingredients:
            ingredients_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredients_ids)
        
        return queryset.filter(
            user = self.request.user
        ).order_by('-id').distinct()
    
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
    