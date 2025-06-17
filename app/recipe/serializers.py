# Serializer for recipe api vid:82-87
from rest_framework import serializers
from core.models import(
    Recipe,
    Tag,
    Ingredient,
)

class IngredientSerializer(serializers.ModelSerializer):
    # serializers for ingredients
    class Meta:
        model = Ingredient
        fields=['id', 'name']
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    # Serializer for tag.

    class Meta:
        model = Tag
        fields=['id', 'name']
        read_only_fields = ['id']

class RecipeSerializer(serializers.ModelSerializer):
    # this serialized is going to represent a specific model
    # in the system and that is our recipe model.
    tags  = TagSerializer(many=True, required=False) #using nested serialize vid-100-105
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'time_minutes', 'price', 'link', 'tags',
            'ingredients',
            ]
        read_only_fields = ['id']
    
    def _get_or_create_tags(self, tags, recipe):
        # Hendle getting  or creating tags for needed.
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag, #tag['name']
            )
            recipe.tags.add(tag_obj)
        
    def _get_or_create_ingredients(self, ingredients, recipe):
        # Hendle getting  or creating ingredients for needed.
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient, #tag['name']
            )
            recipe.ingredients.add(ingredient_obj)


    def create(self, validated_data):
        "create a recipe"
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)
        # auth_user = self.context['request'].user
        # for tag in tags:
        #     tag_obj, created = Tag.objects.get_or_create(
        #         user=auth_user,
        #         **tag, #tag['name']
        #     )
        #     recipe.tags.add(tag_obj)
        return recipe
    
    def update(self, instance, validated_data):
        # update recipe
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance



class RecipeDetailsSerializer(RecipeSerializer):
    # Recipe detail serializers view
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description', 'image']

class RecipeImageSerializer(serializers.ModelSerializer):
    # serializers for uploading images to Recipe
    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fielda = ['id']
        extra_kwargs = {'image': {'required': 'True'}}