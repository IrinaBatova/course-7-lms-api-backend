from rest_framework.pagination import PageNumberPagination


class CoursePaginator(PageNumberPagination):
    page_size = 5 # Количество курсов на одной странице по умолчанию
    page_size_query_param = 'page_size' # Позволяет клиенту передать ?page_size=10 в URL
    max_page_size = 50 # Максимальный лимит элементов, который может запросить клиент


class LessonPaginator(PageNumberPagination):
    page_size = 5  # Количество уроков на одной странице по умолчанию
    page_size_query_param = 'page_size'  # Позволяет клиенту передать ?page_size=10 в URL
    max_page_size = 50  # Максимальный лимит элементов, который может запросить клиент
