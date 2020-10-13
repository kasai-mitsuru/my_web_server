import socket

from ServerThread import ServerThread


class Main:
    @staticmethod
    def main():
        server_socket = socket.socket()
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind the socket to a public host, and a well-known port
        server_socket.bind(("localhost", 8080))
        # become a server socket
        server_socket.listen(10)

        while True:
            print("Main: クライアントからの接続を待ちます。")
            (client_socket, address) = server_socket.accept()
            print("Main: クライアント接続完了")

            thread = ServerThread(client_socket=client_socket)
            thread.start()


if __name__ == '__main__':
    Main().main()
