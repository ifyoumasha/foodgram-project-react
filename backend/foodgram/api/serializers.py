import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (CharField, ImageField, ModelSerializer,
                                        SerializerMethodField, ValidationError)
from rest_framework.status import HTTP_400_BAD_REQUEST

from recipes.models import (Basket, Favorites, Ingredient, Recipe,
                            RecipeIngredientRelations, RecipeTagRelations, Tag)
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
    id = CharField(source='ingredient.id')
    name = CharField(source='ingredient.name')
    measurement_unit = CharField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredientRelations
        fields = ('id', 'name', 'measurement_unit', 'amount')


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeAnotherSerializer(ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
        read_only=True,
        source='recipeingredientrelations_set',
    )
    author = CustomUserSerializer(read_only=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):
        tags = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            RecipeTagRelations.objects.create(tag_id=tag, recipe=recipe)
        for ingredient in ingredients:
            RecipeIngredientRelations.objects.create(
                ingredient_id=ingredient['id'],
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
        tags = self.initial_data.get('tags')
        RecipeTagRelations.objects.filter(recipe=instance).delete()
        for tag in tags:
            RecipeTagRelations.objects.create(tag_id=tag, recipe=instance)
        ingredients = self.initial_data.get('ingredients')
        RecipeIngredientRelations.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            RecipeIngredientRelations.objects.create(
                ingredient_id=ingredient['id'],
                recipe=instance,
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

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        if not ingredients:
            raise ValidationError(
                {'ingredients': ('В рецепт необходимо добавить '
                                 'хотя бы один ингредиент.')
                 }
            )
        array_of_ingredients = []
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient, pk=ingredient['id']
            )
            if current_ingredient in array_of_ingredients:
                raise ValidationError(
                    detail='Ингредиенты в рецепте не должны повторяться.',
                    code=HTTP_400_BAD_REQUEST
                )
            if int(ingredient['amount']) < 1:
                raise ValidationError(
                    {'ingredients': ('Количество ингредиентов в рецепте '
                                     'должно быть больше или равно одному.')
                     }
                )
        if not tags:
            raise ValidationError(
                {'tags': ('Рецепт обязательно должен быть привязан '
                          'хотя бы к одному тегу.')
                 }
            )
        array_of_tags = set(tags)
        if len(array_of_tags) != len(tags):
            raise ValidationError(
                detail='Теги в рецепте не должны повторяться.',
                code=HTTP_400_BAD_REQUEST
            )
        return data
