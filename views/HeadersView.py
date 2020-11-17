from my_http.Request import Request
from my_http.Response import Response, HTTP_STATUS
from views.BaseView import BaseView


class HeadersView(BaseView):
    def get(self, request: Request) -> Response:
        """
        リクエストメソッドがGETだった時の処理
        """

        body_str = ""
        for key, value in request.headers.items():
            body_str += f"{key}: {value}<br>"

        return Response(status=HTTP_STATUS.OK, body=body_str.encode())
