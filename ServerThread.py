import os
import socket
import traceback
from datetime import datetime
from threading import Thread


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

    def __init__(self, client_socket: socket):
        super().__init__()
        self.socket = client_socket

    def run(self):
        print("Worker: 処理開始")
        try:
            # クライアントから受け取ったメッセージを代入
            msg = self.socket.recv(4096)

            print(f"######## received message ##########\n{msg.decode()}")

            # リクエストパス
            path = msg.decode().split("\r\n")[0].split()[1]
            path = os.path.normpath(path)  # 正規化する
            # パスの拡張子
            ext = path.rsplit(".", maxsplit=1)[1] if ("." in path) else ""

            # 送り返す用のメッセージをファイルから読み込む
            http_status = "200 OK"
            data = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
            content_type = self.get_content_type(ext)
            body = b""
            try:
                print(f"file: {self.DOCUMENT_ROOT + path}")
                with open(self.DOCUMENT_ROOT + path, "rb") as f:
                    body = f.read()
            except OSError as e:
                print(f"Worker: ファイルの取得に失敗しました。 error={e}")
                http_status = "404 Not Found"

            output = ""
            output += f"HTTP/1.1 {http_status}\n"
            output += f"Date: {data}\n"
            output += "Server: Modoki/0.1\n"
            output += f"ContentType: {content_type}\n"
            output += "Connection: Close\n"
            output += "\n"

            output_bytes = output.encode() + body

            # メッセージを送り返す
            self.socket.send(output_bytes)

        except Exception:
            print("Worker: " + traceback.format_exc())

        finally:
            self.socket.close()
            print("Worker: 通信を終了しました")

    def get_content_type(self, ext: str):
        if ext != "" or ext not in self.CONTENT_TYPE_MAP:
            return "application/octet-stream"

        return self.CONTENT_TYPE_MAP[ext]
