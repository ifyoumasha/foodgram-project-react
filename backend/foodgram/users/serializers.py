from re import match

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import SerializerMethodField, ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST

from users.models import Follow

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
        return value


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
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user,
            author=obj
        ).exists()


class FollowSerializer(CustomUserSerializer):
    """Кастомный сериализатор для работы с подписками."""
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

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

    def validate(self, data):
        user = self.context.get('request').user
        author = self.instance
        if user == author:
            raise ValidationError(
                detail='Пользователь не может подписаться сам на себя.',
                code=HTTP_400_BAD_REQUEST
            )
        if Follow.objects.filter(
            user=user,
            author=author
        ).exists():
            raise ValidationError(
                detail=('Нельзя подписаться на другого '
                        'пользователя ещё раз.'),
                code=HTTP_400_BAD_REQUEST
            )
        return data

    def get_recipes(self, obj):
        from api.serializers import RecipeAnotherSerializer
        recipes = obj.recipes.all()
        serializers = RecipeAnotherSerializer(
            recipes,
            many=True,
            read_only=True
        )
        return serializers.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
