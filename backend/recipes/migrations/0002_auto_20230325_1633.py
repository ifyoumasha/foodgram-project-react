# Generated by Django 2.2.19 on 2023-03-25 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipe', through='recipes.RecipeIngredientRelations', to='recipes.Ingredient', verbose_name='Ингредиент'),
        ),
    ]
