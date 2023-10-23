from rest_framework.pagination import PageNumberPagination


class DefaultPaginator(PageNumberPagination):
    """Класс реализует пагинацию"""
    page_size = 10
