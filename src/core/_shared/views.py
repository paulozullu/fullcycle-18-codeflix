from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from http import HTTPStatus


class BaseViewSet(viewsets.ViewSet):
    list_use_case = None
    list_serializer_class = None
    repository = None
    order_by_param = "order_by"
    current_page_param = "current_page"
    default_order_by = "name"
    default_current_page = 1

    def list(self, request: Request) -> Response:
        order_by = request.query_params.get(self.order_by_param, self.default_order_by)
        current_page = int(
            request.query_params.get(self.current_page_param, self.default_current_page)
        )
        input_data = self.list_use_case.Input(
            order_by=order_by, current_page=current_page
        )
        use_case = self.list_use_case(repository=self.repository())
        output = use_case.execute(input_data)
        serializer = self.list_serializer_class(output)
        return Response(status=HTTPStatus.OK, data=serializer.data)
