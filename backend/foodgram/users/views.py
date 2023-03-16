from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from users.models import Follow
from users.serializers import CustomUserSerializer, FollowSerializer

User = get_user_model()


class UserFollowViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False)
    def subscriptions(self, request):
        follows = User.objects.filter(following__user=request.user)
        pages = self.paginate_queryset(follows)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        if request.method == 'POST':
            serializer = FollowSerializer(
                author,
                data=request.data,
                context={'request': request}
            )
            if not serializer.is_valid():
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            Follow.objects.create(
                user=request.user,
                author=author
            )
            return Response(serializer.data, status=HTTP_201_CREATED)
        follow = get_object_or_404(Follow, user=request.user, author=author)
        follow.delete()
        return Response(status=HTTP_204_NO_CONTENT)
