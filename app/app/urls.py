"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# http://127.0.0.1:8000/api/docs/#/user/user_token_create
# http://127.0.0.1:8000/admin/core/user/add/
from django.contrib import admin
from django.urls import path, include # The URLs module allows us to include URLs from a different app.
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name = 'api-schema'),
    # So this is going to add a euro to our project that uses this spectacular API view.
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api_docs',
    ),
    # Then we have API forward slash docs that will serve the swagger documentation that is going to use our
    # schema to generate a graphical user interface for our API documentation.
    path('api/user/', include('user.urls')),
    path('api/recipe', include('recipe.urls')),
]
