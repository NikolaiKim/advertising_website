from rest_framework.pagination import PageNumberPagination


# Создаем постраничный вывод для объявлений по 4 шт на страницу
class AdvertPaginator(PageNumberPagination):
    page_size = 4
    page_query_param = 'page_size'
    max_page_size = 50
