from rest_framework.pagination import PageNumberPagination

# pagination class for search 
class SearchPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 6


# pagination class for filtered products
class FilteredProductsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 12
