from django.http import JsonResponse
from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response


class GoodResponse(Response):
    def __init__(
        self,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        if isinstance(data, dict):
            data.update({"success": True})
            new_data = data
        else:
            new_data = {"success": True, "data": data}
        super().__init__(
            new_data, status, template_name, headers, exception, content_type
        )


class BadResponse(Response):
    def __init__(
        self,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        if isinstance(data, dict):
            data.update({"success": False})
            new_data = data
        else:
            new_data = {"success": False, "data": data}
        super().__init__(
            new_data, status, template_name, headers, exception, content_type
        )


def format_success_reponse(data, code=200):
    response = {"code": code, "success": True, "data": data}
    return JsonResponse(response, status=code, safe=False)


def format_failure_reponse(data, code=400):
    response = {"code": code, "success": False, "data": data}
    return JsonResponse(response, status=code, safe=False)


class CustomPageNumberPagination(PageNumberPagination):
    DEFAULT_PAGE: int = 1
    page: int = DEFAULT_PAGE
    page_size: int = 10
    page_size_query_param = "page_size"
    max_page_size: int = 100
    daily_limit: int = 0
    current_count_today: int = 0

    def get_paginated_response(self, data):
        response_result = OrderedDict(
            [
                ("total_page", self.page.paginator.num_pages),
                ("count", self.page.paginator.count),
                ("next", self.get_next_link()),
                ("previous", self.get_previous_link()),
                ("results", data),
                (
                    "currentPage",
                    int(
                        self.request.GET.get("page", self.DEFAULT_PAGE)
                    ),  # can not set default = self.page
                ),
            ]
        )
        if self.daily_limit:
            response_result["daily_limit"] = self.daily_limit
        if self.current_count_today:
            response_result["current_count_today"] = self.current_count_today
        return Response(response_result)

    def get_paginated_response_revised(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "itemsCount": self.page.paginator.count,
                "currentPage": int(
                    self.request.GET.get("page", self.DEFAULT_PAGE)
                ),  # can not set default = self.page
                "page_size": int(
                    self.request.GET.get(self.page_size_query_param, self.page_size)
                ),
                "totalPages": self.page.paginator.num_pages,
                "results": data,
            }
        )


class CustomPaginator:
    def __init__(self, **kwargs):
        request = kwargs.get("request")
        pagination_type = kwargs.get("pagination_type", "PNP")
        query_set = kwargs.get("query_set")
        serializer = kwargs.get("serializer")
        if pagination_type == "PNP":
            max_page_size = kwargs.get("max_page_size", 50)
            page_size = kwargs.get("page_size", 1)
            current_count_today = kwargs.get("current_count_today", 0)
            daily_limit = kwargs.get("daily_limit", 0)
            paginator = CustomPageNumberPagination()
            paginator.current_count_today = current_count_today
            paginator.daily_limit = daily_limit
            context = paginator.paginate_queryset(query_set, request)
            ser = serializer(context, many=True)
            self.data = paginator.get_paginated_response(ser.data)
        else:
            # paginator is LOP
            max_page_size = kwargs.get("max_page_size", 50)
            page_size = kwargs.get("page_size", 20)
            lim_paginator = LimitOffsetPagination()
            lim_paginator.max_limit = max_page_size
            lim_paginator.default_limit = page_size
            lim_context = lim_paginator.paginate_queryset(query_set, request)
            lim_serializer = serializer(lim_context, many=True)
            self.data = lim_paginator.get_paginated_response(lim_serializer.data)
