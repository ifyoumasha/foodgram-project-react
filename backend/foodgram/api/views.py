from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import (IngredientSerializer, RecipeAnotherSerializer,
                             RecipeIngredientRelations, RecipeSerializer,
                             TagSerializer)
from recipes.models import Basket, Ingredient, Favorites, Recipe, Tag


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False)
    def download_shopping_cart(self, request):
        if not Basket.objects.filter(
                user=request.user
        ).exists():
            return Response(
                {'errors': 'В Корзине отсутствуют рецепты'},
                status=HTTP_400_BAD_REQUEST
            )
        ingredients = RecipeIngredientRelations.objects.filter(
            recipe__baskets__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        shopping_list = ''
        for ingredient in ingredients:
            item = (f'* {ingredient["ingredient__name"]} '
                    f'({ingredient["ingredient__measurement_unit"]}) -- '
                    f'{ingredient["amount"]}\n\n'
                    )
            shopping_list += item
        response = HttpResponse(shopping_list,
                                content_type='text/plain;charset=UTF-8'
                                )
        return response

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = RecipeAnotherSerializer(recipe)
            if Basket.objects.filter(
                user=request.user,
                recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт уже есть в корзине.'},
                    status=HTTP_400_BAD_REQUEST
                )
            Basket.objects.create(
                user=request.user,
                recipe=recipe
            )
            return Response(serializer.data, status=HTTP_201_CREATED)
        if not Basket.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists():
            return Response(
                {'errors': 'Рецепт отсутствует в корзине.'},
                status=HTTP_400_BAD_REQUEST
            )
        Basket.objects.filter(
            user=request.user,
            recipe=recipe
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = RecipeAnotherSerializer(recipe)
            if Favorites.objects.filter(
                user=request.user,
                recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт уже есть в избранном.'},
                    status=HTTP_400_BAD_REQUEST
                )
            Favorites.objects.create(
                user=request.user,
                recipe=recipe
            )
            return Response(serializer.data, status=HTTP_201_CREATED)
        if not Favorites.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists():
            return Response(
                {'errors': 'Рецепт отсутствует в избранном.'},
                status=HTTP_400_BAD_REQUEST
            )
        Favorites.objects.filter(
            user=request.user,
            recipe=recipe
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)
