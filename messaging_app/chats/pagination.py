from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'  # optional: allow client to control page size (up to max_page_size)
    max_page_size = 100

    def get_paginated_response(self, data):
        total_count = self.page.paginator.count  # total items in the queryset
        return Response({
            'count': total_count,
            'page_size': self.get_page_size(self.request),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
