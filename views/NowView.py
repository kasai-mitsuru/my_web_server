from datetime import datetime

from my_http.Request import Request
from my_http.Response import Response, HTTP_STATUS
from views.BaseView import BaseView


class NowView(BaseView):
    def get(self, request: Request) -> Response:
        """
        リクエストメソッドがGETだった時の処理
        """
        body = f"""\
        <html>
        <body>
            now is {datetime.now()}
        </body>
        </html>
        """.encode()
        return Response(status=HTTP_STATUS.OK, body=body)
