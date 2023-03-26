from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.viewsets import GenericViewSet


class CustomRecipeViewSet(CreateModelMixin, DestroyModelMixin,
                          ListModelMixin, RetrieveModelMixin,
                          UpdateModelMixin, GenericViewSet):
    pass
