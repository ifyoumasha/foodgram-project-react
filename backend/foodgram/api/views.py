from rest_framework.viewsets import ReadOnlyModelViewSet

from recipes.models import Tag, Ingredient
from api.serializers import TagSerializer, IngredientSerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
