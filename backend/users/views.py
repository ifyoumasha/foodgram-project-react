from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from users.models import Subscription
from users.serializers import CustomUserSerializer, FollowSerializer

User = get_user_model()


class UserFollowViewSet(UserViewSet):
    """
    Вьюсет для модели Пользователя с обработкой запросов
    на создание и удаление подписки.
    """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        follows = User.objects.filter(following__user=request.user)
        pages = self.paginate_queryset(follows)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(IsAuthenticated,),
        url_path='subscribe'
    )
    def add_subscribe(self, request, **kwargs):
        user = request.user
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        serializer = FollowSerializer(
            author,
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        Subscription.objects.create(
            user=user,
            author=author
        )
        return Response(serializer.data, status=HTTP_201_CREATED)

    @add_subscribe.mapping.delete
    def destroy_subscribe(self, request, **kwargs):
        user = request.user
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        if not Subscription.objects.filter(
            user=user,
            author=author
        ).exists():
            return Response(
                {'errors': 'Подписки не существует.'},
                status=HTTP_400_BAD_REQUEST
            )
        Subscription.objects.filter(
            user=request.user,
            author=author
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)
