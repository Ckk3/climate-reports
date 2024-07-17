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


def test_tcp_server_response_should_create_new_user():
    message = "joao,joao@nimbusmeteorologia.com.br,01234567891,34"
    response = send_message_to_server(message)
    assert response == "Ok"


def test_tcp_server_response_should_not_create_new_user_when_format_is_invalid():
    message = "invalidjoao,joao@nimbusmeteorologia.com.br,01234567891,34,aa"
    response = send_message_to_server(message)
    assert response == "Error: please send the data with the following format: 'name,email,phone,age'"

    message = "invalidjoao,joao@nimbusmeteorologia.com.br,01234567891"
    response = send_message_to_server(message)
    assert response == "Error: please send the data with the following format: 'name,email,phone,age'"
