from django.contrib import admin
from django.contrib.admin import ModelAdmin

from recipes.models import (Favorites,
                            Ingredient,
                            Recipe,
                            RecipeIngredientRelations,
                            RecipeTagRelations,
                            ShoppingCart,
                            Tag)


class TagAdmin(ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name',)


class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author', 'count_favorites')
    list_filter = ('author', 'name', 'tags')

    def count_favorites(self, obj):
        return obj.favorites.count()


class RecipeTagRelationsAdmin(ModelAdmin):
    list_display = ('tag', 'recipe')
    list_filter = ('tag', 'recipe')


class RecipeIngredientRelationsAdmin(ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount')
    list_filter = ('ingredient', 'recipe')


class FavoritesAdmin(ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')


class ShoppingCartAdmin(ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeTagRelations, RecipeTagRelationsAdmin)
admin.site.register(RecipeIngredientRelations, RecipeIngredientRelationsAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
