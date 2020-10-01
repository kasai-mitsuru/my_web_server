import socket


class TcpClient:
    def main(self):
        clientsocket = socket.socket()

        clientsocket.connect(('abehiroshi.la.coocan.jp', 80))

        with open("client_send.txt", "rb") as f:
            msg = f.read()

        clientsocket.send(msg)

        msg = clientsocket.recv(4096)
        with open("client_recv.txt", "wb") as f:
            f.write(msg)

        clientsocket.close()



if __name__ == '__main__':
    TcpClient().main()