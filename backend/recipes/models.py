from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        'Название тега',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        'Цвет тега',
        max_length=7,
        null=True,
        unique=True
    )
    slug = models.SlugField(
        max_length=200,
        null=True,
        unique=True
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        'Название ингредиента',
        max_length=200)
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200)
    image = models.ImageField(
        'Картинка рецепта',
        upload_to='recipes/')
    text = models.TextField('Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientRelations',
        related_name='recipe',
        verbose_name='Ингредиент'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTagRelations',
        verbose_name='Тег'
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        validators=[MinValueValidator(1), ]
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeTagRelations(models.Model):
    """Модель для связывания Recipe и Tag через поле ManyToManyField."""
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег, связанный с рецептом'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт, связанный с тегом'
    )

    class Meta:
        verbose_name = 'Связь тегов и рецептов'
        verbose_name_plural = 'Связь тегов и рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'recipe'],
                name='Необходима уникальная связь между рецептом и тегом.'
            )
        ]

    def __str__(self):
        return f"Тег {self.tag} для рецепта {self.recipe}"


class RecipeIngredientRelations(models.Model):
    """Модель для связывания Recipe и Ingredient через поле ManyToManyField."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Ингредиент, связанный с рецептом'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт, связанный с ингредиентом'
    )
    amount = models.PositiveIntegerField(
        'Количество ингредиентов',
        validators=[MinValueValidator(1), ]
    )

    class Meta:
        verbose_name = 'Связь ингредиентов и рецептов'
        verbose_name_plural = 'Связь ингредиентов и рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='Связь рецепта и ингредиента должна быть уникальной.'
            )
        ]

    def __str__(self):
        return f"Ингредиент {self.ingredient} для рецепта {self.recipe}"


class Favorites(models.Model):
    """Модель для добавления рецептов в избранное."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь, добавляющий рецепты в избранное'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт, добавленный в избранное'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='Нельзя повторно добавлять рецепт в избранное.'
            )
        ]

    def __str__(self):
        return f"({self.user} добавил рецепт {self.recipe} в избранное.)"


class ShoppingCart(models.Model):
    """Модель для добавления рецептов в корзину."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь, добавляющий рецепты в корзину'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепты, добавленные в корзину'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='Нельзя повторно добавлять рецепт в корзину.'
            )
        ]

    def __str__(self):
        return f"({self.user} добавил рецепт {self.recipe} в корзину.)"
