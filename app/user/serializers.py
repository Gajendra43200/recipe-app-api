# Serializers for user api vid: 68-71
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _ # import as underscore because that is the common syntax for doing the translations with Django.

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    # serializers for user objects 
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {"write_only": True, 'min_length': 5}}
        # And that is a dictionary that allows us to provide extra metadata to the different fields.
    
    def create(self, validate_data): #The Create method allows us to override the behavior
        #  that the serialize it does when you create new
        # objects out of that serialize.
        # Created and return user with encripted password 
        return get_user_model().objects.create_user(**validate_data)
    # So serialize is simply just a way to convert objects to and from python objects.
    # They allow us to automatically validate and save things to a specific model that we define in our serialization.

    def update(self, instance, validated_data):
        # Update and return user 
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data) # And this is going to perform all of the steps for updating the object.

        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg= ('Unable  to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs