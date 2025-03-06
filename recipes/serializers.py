from rest_framework import serializers
from . models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Recipe
        fields='__all__'

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    pasword=serializers.CharField()       