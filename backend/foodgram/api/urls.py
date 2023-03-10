from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.views import TagViewSet, IngredientViewSet


router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
# router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
