from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    Кастомный пагинатор фиксирующий количество результатов
    в выдаче на странице пользователя.
    """
    page_size_query_param = 'limit'
    page_size = 6
