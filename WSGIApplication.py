from enum import Enum
from typing import Callable, List, Iterable


# noinspection PyPep8Naming
class HTTP_STATUS_CODE(Enum):
    OK = "200 OK"
    NOT_FOUND = "404 Not Found."
    SERVER_ERROR = "500 Internal Server Error"


class WSGIApplication:
    env: dict
    start_response: Callable[[str, List[tuple]], None]

    DOCUMENT_ROOT = "./resources"
    DOCUMENT_404 = "./resources/404.html"

    def application(self, env: dict, start_response: Callable[[str, Iterable[tuple]], None]):
        """
        env:
            リクエストヘッダーの情報がdictで渡されてくる
            refs) https://www.python.org/dev/peps/pep-3333/#environ-variables
            例）
            env = {
                "HTTP_METHOD": "POST",
                "PATH_INFO": "/index.html"
            }

        start_response:
            レスポンスヘッダーの内容を、WSGIサーバーへ伝えるための関数(or Callable)。
            WSGIアプリケーション内で一度だけコールする。
            コールするときは、第一引数にレスポンスライン、第２引数にレスポンスヘッダーを渡してコールする。
            例）
            start_response(
                '200 OK',
                [
                    ('Content-type', 'text/plain; charset=utf-8'),
                    ('Connection', 'Closed')
                ]
            )
        """
        self.env = env
        self.start_response = start_response

        try:
            path = env["PATH_INFO"]
            try:
                return self.start_ok([self.get_file_content(path)])

            except OSError:
                return self.start_not_found()

        except Exception:
            return self.start_server_error()

    def get_file_content(self, path: str) -> bytes:
        with open(self.DOCUMENT_ROOT + path, "rb") as f:
            return f.read()

    def start_ok(self, body: Iterable[bytes]) -> Iterable[bytes]:
        status = HTTP_STATUS_CODE.OK
        self.start_response(str(status), [])

        return body

    def start_not_found(self) -> Iterable[bytes]:
        status = HTTP_STATUS_CODE.NOT_FOUND
        self.start_response(str(status), [("Content-Type", "text/html")])

        with open(self.DOCUMENT_404, "rb") as f:
            return [f.read()]

    def start_server_error(self) -> Iterable[bytes]:
        status = HTTP_STATUS_CODE.SERVER_ERROR
        self.start_response(str(status), [("Content-Type", "text/html")])

        return [b"<html><body><h1>500 Internal Server Error</h1></body></html>"]
