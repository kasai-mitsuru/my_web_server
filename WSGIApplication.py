from datetime import datetime
from enum import Enum
from typing import Callable, List, Iterable, Dict


# noinspection PyPep8Naming
class HTTP_STATUS(Enum):
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

            if path == '/now':
                body_str = f"<html><body><h1>now is {datetime.now()}</h1></body></html>"

                self.start_ok(headers={"Content-Type": "text/html"})
                return [body_str.encode()]

            if path == '/headers':
                body_str = "<html><body>"
                for key, value in env.items():
                    body_str += f"{key}: {value}<br>"
                body_str += "<body><html>"

                self.start_ok(headers={"Content-Type": "text/html"})
                return [body_str.encode()]

            try:
                body = self.get_file_content(path)
                self.start_ok()
                return [body]

            except OSError:
                with open(self.DOCUMENT_404, "rb") as f:
                    self.start_not_found()
                    return [f.read()]

        except Exception:
            self.start_server_error()
            return [b"<html><body><h1>500 Internal Server Error</h1></body></html>"]

    def get_file_content(self, path: str) -> bytes:
        with open(self.DOCUMENT_ROOT + path, "rb") as f:
            return f.read()

    def start_ok(self, headers: Dict[str, str] = None) -> None:
        if headers is None:
            headers = {}

        status = HTTP_STATUS.OK
        self.start_response(str(status), [(key, value) for key, value in headers.items()])

    def start_not_found(self) -> None:
        status = HTTP_STATUS.NOT_FOUND
        self.start_response(str(status), [("Content-Type", "text/html")])

    def start_server_error(self) -> None:
        status = HTTP_STATUS.SERVER_ERROR
        self.start_response(str(status), [("Content-Type", "text/html")])
