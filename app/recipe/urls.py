# URls mapping for the recipe app 
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter
from recipe import views
from recipe.views import TagViewSet
from recipe.views import IngredientViewSet

router = DefaultRouter()
router.register('recipe', views.RecipeViewSet)
# the functionality that's enabled on the view set.
# Because we're using the model view set, it's
# going to support all the available methods for create,
# read, update and delete those.
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
app_name = 'recipe'
# define the name which is used to identify the name when we're doing the reverse lookup of URLs.

urlpatterns = [
    path('', include(router.urls)),
    # this up inside the main URLs so that we can actually
    # access it.
]

# And then here in the URL patterns, we're using the include function to include the URLs that are generated
# automatically by the router.
# Add the file inside the app urls.py file: path('api/recipe', include('recipe.urls')),

