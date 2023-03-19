from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserFollowViewSet

app_name = 'users'

router = DefaultRouter()
router.register('users', UserFollowViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
