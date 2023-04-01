from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import ReadOnlyModelViewSet

from recipes.filters import RecipeFilterSet
from recipes.mixins import CustomRecipeViewSet
from recipes.models import Favorites, Ingredient, Recipe, ShoppingCart, Tag
# from recipes.permissions import IsAuthorOrReadOnly
from recipes.serializers import (IngredientSerializer,
                                 FavoritesSerializer,
                                 RecipeIngredientRelations,
                                 RecipeSerializer,
                                 ShoppingCartSerializer,
                                 TagSerializer)


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для модели Тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для модели Ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)

    def get_queryset(self):
        name = self.request.query_params['name'].lower()
        starts_with_queryset = list(
            self.queryset.filter(name__istartswith=name)
        )
        cont_queryset = self.queryset.filter(name__icontains=name)
        starts_with_queryset.extend(
            [x for x in cont_queryset if x not in starts_with_queryset]
        )
        return starts_with_queryset


class RecipeViewSet(CustomRecipeViewSet):
    """
    Вьюсет для модели Рецептов с обработкой запросов для добавления рецептов
    в избранное и корзину, а также для скачивания списка покупок.
    """
    queryset = Recipe.objects.all()
    # permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(IsAuthenticated,),
        url_path='favorite'
    )
    def add_recipes_in_favorites(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorites_data = {
            'user': user.id,
            'recipe': recipe.id
        }
        serializer = FavoritesSerializer(
            data=favorites_data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    @add_recipes_in_favorites.mapping.delete
    def destroy_recipes_from_favorites(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        Favorites.objects.filter(
            user=user,
            recipe=recipe
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(IsAuthenticated,),
        url_path='shopping_cart'
    )
    def add_recipes_in_shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_cart_data = {
            'user': user.id,
            'recipe': recipe.id
        }
        serializer = ShoppingCartSerializer(
            data=shopping_cart_data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    @add_recipes_in_shopping_cart.mapping.delete
    def destroy_recipes_from_shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        ShoppingCart.objects.filter(
            user=user,
            recipe=recipe
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['get'],
            detail=False,
            permission_classes=(IsAuthenticated,),
            url_path='download_shopping_cart')
    def download_ingredient_list(self, request):
        user = request.user
        if not user.shopping_cart:
            return Response(
                {'errors': 'Пользователь не добавил в корзину'
                           'ни одного рецепта.'},
                status=HTTP_400_BAD_REQUEST
            )
        ingredients = RecipeIngredientRelations.objects.filter(
            recipe__shopping_cart__user=user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        ingredient_list = 'Ингредиенты для избранных рецептов:\n\n'
        for ingredient in ingredients:
            item = (f'~ {ingredient["ingredient__name"]} - '
                    f'{ingredient["amount"]} '
                    f'({ingredient["ingredient__measurement_unit"]})\n\n'
                    )
            ingredient_list += item
        footer = 'Foodgram 2023\nХороших покупок!'
        ingredient_list += footer
        return HttpResponse(ingredient_list,
                            content_type='text/plain;charset=UTF-8')
