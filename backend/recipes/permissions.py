from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Кастомный пермишн для админа или для чтения.
    """
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user or
                request.method in SAFE_METHODS or
                request.user.is_staff
                )


class IsAuthorOrReadOnly(BasePermission):
    """
    Кастомный пермишн для автора рецепта или для чтения.
    """
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user or
                request.method in SAFE_METHODS or
                request.user.is_staff
                )


class IsAuthenticatedOrAdmin(BasePermission):
    """
    Кастомный пермишн для авторизованного пользователя или админа.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated or request.user.is_staff
