# Serializer for recipe api vid:82-87
from rest_framework import serializers
from core.models import(
    Recipe,
    Tag,
)

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

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
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


    def create(self, validate_data):
        "create a recipe"
        tags = validate_data.pop('tags', [])
        recipe = Recipe.objects.create(**validate_data)
        self._get_or_create_tags(tags, recipe)
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
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance



class RecipeDetailsSerializer(RecipeSerializer):
    # Recipe detail serializers view
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
        