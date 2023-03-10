from rest_framework.viewsets import ReadOnlyViewSet

from recipes.models import Tag, Ingredient
from api.serializers import TagSerializer, IngredientSerializer


class TagViewSet(ReadOnlyViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
