import re
import socket
import traceback
from threading import Thread
from typing import List, Iterable, Dict, Tuple

from WSGIApplication import WSGIApplication


class ServerThread(Thread):
    DOCUMENT_ROOT = "/Users/mitsuru_kasai/Documents/github/my_web_server/docs"
    CONTENT_TYPE_MAP = {
        "html": "text/html",
        "htm": "text/html",
        "txt": "text/plain",
        "css": "text/css",
        "js": "application/javascript",
        "png": "image/png",
        "jpg": "image/jpg",
        "jpeg": "image/jpg",
        "gif": "image/gif",
    }

    response_line: str
    response_headers: List[tuple]

    def __init__(self, client_socket: socket):
        super().__init__()
        self.socket = client_socket

    def run(self):
        print("Worker: 処理開始")
        try:
            # クライアントから受け取ったメッセージを代入
            request = self.socket.recv(4096)
            request_decoded: str = request.decode()

            print(f"######## received message ##########\n{request_decoded}")

            # requestをパースする
            method, path, protocol, request_headers, request_body = self.parse_request(request_decoded)

            # WSGI Application用のenvを生成
            env = self.build_env(method, path, protocol, request_headers, request_body)

            # WSGI Application用のstart_responseを生成
            def start_response(response_line: str, response_headers: List[tuple]):
                self.response_line = response_line
                self.response_headers = response_headers

            # WSGIアプリケーションのapplicationを呼び出す
            body_bytes_list: Iterable[bytes] = WSGIApplication().application(env, start_response)

            # 呼び出し結果をもとにレスポンスを生成する
            output_bytes = b""
            output_bytes += self.get_response_header()
            output_bytes += "\r\n".encode()
            output_bytes += self.get_response_body(body_bytes_list)

            print(f"######## send message ##########\n{output_bytes.decode()}")

            self.socket.send(output_bytes)

        except Exception:
            print("Worker: " + traceback.format_exc())

        finally:
            self.socket.close()
            print("Worker: 通信を終了しました")

    def parse_request(self, request: str) -> Tuple[str, str, str, Dict[str, str], str]:
        # request_lineを抽出
        request_line, remain = request.split("\r\n", maxsplit=1)
        # メソッド、パス、プロトコルを取得
        method, path, protocol = request_line.split(" ", maxsplit=2)
        # request headerを抽出、パース
        header_str, body = remain.split("\r\n\r\n", maxsplit=1)
        headers = self.parse_headers(header_str)

        return method, path, protocol, headers, body

    @staticmethod
    def parse_headers(header_str: str) -> Dict[str, str]:
        header_lines = header_str.split("\r\n")
        header_tuples = (tuple(re.split(r": *", header_line, maxsplit=1)) for header_line in header_lines)
        return {
            header_tuple[0]: header_tuple[1]
            for header_tuple
            in header_tuples
        }

    @staticmethod
    def build_env(method: str, path: str, protocol: str, headers: Dict[str, str], body: str) -> dict:
        split_path = path.split("?", maxsplit=1)
        env = {
            "REQUEST_METHOD": method.upper(),
            "PATH_INFO": split_path[0],
            "QUERY_STRING": split_path[1] if len(split_path) > 1 else "",
            "SERVER_PROTOCOL": protocol,
            "CONTENT_TYPE": headers.get("Content-Type", "")
        }

        # HTTP_Variables
        for header_key, header_value in headers.items():
            key = "HTTP_" + header_key.upper().replace("-", "_")
            env[key] = header_value

        print(f"env: {env}")

        return env

    def get_content_type(self, ext: str):
        if ext != "" or ext not in self.CONTENT_TYPE_MAP:
            return "application/octet-stream"

        return self.CONTENT_TYPE_MAP[ext]

    # noinspection SpellCheckingInspection
    def get_response_header(self) -> bytes:
        # ex) "HTTP/1.1 200 OK"
        status_line = "HTTP/1.1 " + self.response_line + "\r\n"

        # ex)
        # self.response_headers = [("key1", "value1"), ("key2, value2")]
        # header_text_list = ["key1: value1", "key2: value2"]
        # header_text = "key1: value1\r\nkey2: value2"
        header_text_list = (": ".join(response_header) for response_header in self.response_headers)
        header_text = "\r\n".join(header_text_list) + "\r\n"

        header = b""
        header += status_line.encode()
        header += header_text.encode()
        return header

    @staticmethod
    def get_response_body(body_bytes_list: Iterable[bytes]) -> bytes:
        return b"".join(body_bytes_list)
