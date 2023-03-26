import base64

from django.core.files.base import ContentFile
from rest_framework.serializers import (CharField, ImageField, ModelSerializer,
                                        SerializerMethodField)

from recipes.models import (Favorites, Ingredient, Recipe,
                            RecipeIngredientRelations, RecipeTagRelations,
                            ShoppingCart, Tag)
from users.serializers import CustomUserSerializer


class TagSerializer(ModelSerializer):
    """Сериализатор для модели Тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(ModelSerializer):
    """Сериализатор для модели Ингредиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(ModelSerializer):
    """Сериализатор для связанной модели Рецептов и Ингредиентов."""
    id = CharField(source='ingredient.id')
    name = CharField(source='ingredient.name')
    measurement_unit = CharField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredientRelations
        fields = ('id', 'name', 'measurement_unit', 'amount')


class Base64ImageField(ImageField):
    """Класс для добавления изображения при создании рецепта."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeAnotherSerializer(ModelSerializer):
    """Сериализатор для Рецептов с добавлением времени приготовления."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSerializer(ModelSerializer):
    """Сериализатор для модели Рецептов."""
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
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorites.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()
