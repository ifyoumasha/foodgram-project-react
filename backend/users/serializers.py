from re import match

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        ValidationError)

import recipes.serializers
from recipes.models import Recipe
from users.models import Subscription

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Кастомный сериализатор для создания Пользователя."""
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        write_only_fields = ('password',)

    def validate_username(self, value):
        if not match(r'[\w.@+\-]+', value):
            raise ValidationError('Некорректный логин')
        if value == 'me':
            raise ValidationError('Имя пользователя не может быть <me>.')
        return value

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('Такой электронный адрес уже существует.')
        return email


class CustomUserSerializer(UserSerializer):
    """Кастомный сериализатор для работы с пользователем."""
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return not user.is_anonymous and Subscription.objects.filter(
            user=user,
            author=obj
        ).exists()


class FollowSerializer(ModelSerializer):
    """Кастомный сериализатор для работы с подписками."""
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return not user.is_anonymous and Subscription.objects.filter(
            user=user,
            author=obj
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        queryset = obj.recipes.all()
        if recipes_limit:
            queryset = queryset[:int(recipes_limit)]
        serializers = recipes.serializers.RecipeAnotherSerializer(
            queryset,
            many=True,
            read_only=True
        )
        return serializers.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
