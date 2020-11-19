from datetime import datetime
from textwrap import dedent

from my_http.Request import Request
from my_http.Response import Response, HTTP_STATUS
from views.BaseView import BaseView


class SetCookieView(BaseView):
    def get(self, request: Request) -> Response:

        body = dedent(
            f"""
            <html>
            <body>
                <h2>
                    Current Cookies: {request.cookies}
                </h2>
            </body>
            </html>
            """
        ).encode()

        return Response(
            status=HTTP_STATUS.OK, body=body, cookies={"foo": "bar", "foo2": "bar2"}
        )
