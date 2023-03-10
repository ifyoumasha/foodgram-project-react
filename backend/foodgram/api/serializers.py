from rest_framework.serializers import ModelSerializer

from recipes.models import Tag, Ingredient


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('__all__')


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')
