import socket

def send_message_to_server(message):
    server_address = ('localhost', 5784)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(server_address)
        sock.sendall(message.encode('utf-8'))
        response = sock.recv(1024)
        return response.decode('utf-8')
    finally:
        sock.close()


def test_tcp_server_response():
    message = "joao,joao@nimbusmeteorologia.com.br,01234567891,34"
    response = send_message_to_server(message)
    assert response == "Ok"
