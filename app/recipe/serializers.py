# Serializer for recipe api vid:82-87
from rest_framework import serializers
from core.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    # this serialized is going to represent a specific model
    # in the system and that is our recipe model.

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']