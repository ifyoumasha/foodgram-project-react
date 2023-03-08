from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

User = get_user_model()


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        'Название тега',
        max_length=200)
    color = models.CharField(
        'Цвет тега',
        max_length=7,
        null=True
    )
    slug = models.SlugField(
        max_length=200,
        null=True,
        unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        'Название ингредиента',
        max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
        )
    name = models.CharField(
        'Название рецепта',
        max_length=200)
    image = models.ImageField(
        'Картинка рецепта',
        upload_to='recipes/')
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientRelations'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTagRelations'
        )
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1), ]
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeTagRelations(models.Model):
    """Модель для связывания Recipe и Tag через поле ManyToManyField."""
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.tag.__str__()}, {self.recipe.__str__()})"


class RecipeIngredientRelations(models.Model):
    """Модель для связывания Recipe и Ingredient через поле ManyToManyField."""
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1), ]
    )

    def __str__(self):
        return f"({self.ingredient.__str__()}, {self.recipe.__str__()})"


class Favorites(models.Model):
    """Модель для добавления рецептов в избранное."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.user} добавил рецепт {self.recipe} в избранное.)"


class Basket(models.Model):
    """Модель для добавления рецептов в корзину."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.user} добавил рецепт {self.recipe} в корзину.)"
