from rest_framework.pagination import PageNumberPagination


# Создаем постраничный вывод для объявлений по 4 шт на страницу
class FeedbackPaginator(PageNumberPagination):
    page_size = 5
    page_query_param = 'page_size'
    max_page_size = 50
