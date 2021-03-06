from my_http.Request import Request
from my_http.Response import Response, HTTP_STATUS
from views.BaseView import BaseView


class ParametersView(BaseView):
    def get(self, request: Request) -> Response:
        """
        リクエストメソッドがGETだった時の処理
        """
        body = f"""\
        <html>
        <body>
            {str(request.GET)}
        </body>
        </html>
        """.encode()
        return Response(status=HTTP_STATUS.OK, body=body)

    def post(self, request: Request) -> Response:
        """
        リクエストメソッドがPOSTだった時の処理
        """
        body = f"""\
        <html>
        <body>
            {str(request.POST)}
        </body>
        </html>
        """.encode()
        return Response(status=HTTP_STATUS.OK, body=body)
