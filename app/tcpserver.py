from socketserver import TCPServer, BaseRequestHandler
from utils import add_new_user

class TCPHandler(BaseRequestHandler):
    def handle(self):
        # Handle requests with clients info
        data = self.request.recv(1024).strip().decode('utf-8')
        print(f"Data received: {data}")
        try:
            # Add new user to db
            add_new_user(data=data)
            self.request.send('Ok'.encode('utf-8'))
        except Exception as e:
            self.request.send(str(e).encode('utf-8'))


if __name__ == "__main__":
    print("Starting TCP Server")
    HOST, PORT = "0.0.0.0", 5784

    server = TCPServer((HOST, PORT), TCPHandler)
    print(f"Server running in {HOST}:{PORT}...")
    server.serve_forever()
