import base64

from django.core.files.base import ContentFile
from recipes.models import (Basket, Favorites, Ingredient, Recipe,
                            RecipeIngredientRelations, RecipeTagRelations, Tag)
from rest_framework.serializers import (ImageField, ModelSerializer,
                                        SerializerMethodField)
from users.serializers import CustomUserSerializer


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('__all__')


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')


class RecipeIngredientSerializer(ModelSerializer):
    measurement_unit = SerializerMethodField()

    class Meta:
        model = RecipeIngredientRelations
        fields = ('__all__')

    def get_measurement_unit(self, instance):
        return instance.ingredient.measurement_unit


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            RecipeTagRelations.objects.create(tag=tag, recipe=recipe)
        for ingredient in ingredients:
            RecipeIngredientRelations.objects.create(
                ingredient=ingredient['id'],
                recipe=recipe,
                amount=ingredient['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        tags = validated_data.get('tags')
        RecipeTagRelations.objects.filter(recipe=instance.id).delete()
        for tag in tags:
            RecipeTagRelations.objects.create(tag=tag, recipe=instance.id)
        ingredients = validated_data.get('ingredients')
        RecipeIngredientRelations.objects.filter(recipe=instance.id).delete()
        for ingredient in ingredients:
            RecipeIngredientRelations.objects.create(
                ingredient=ingredient['id'],
                recipe=instance.id,
                amount=ingredient['amount']
            )
        instance.save()
        return instance

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favorites.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Basket.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()


class RecipeAnotherSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
