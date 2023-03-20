from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    username = models.CharField(
        'Логин пользователя',
        max_length=150,
        unique=True,
        validators=(UnicodeUsernameValidator(),)
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254)
    first_name = models.CharField(
        'Имя пользователя',
        max_length=150)
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=150)
    password = models.CharField(
        'Пароль пользователя',
        max_length=150)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
    """Модель для подписки на пользователя."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    def __str__(self):
        return f'{self.user} подписался на {self.author}.'

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='user_cannot_follow_himself'
            ),
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following'
            )
        ]
