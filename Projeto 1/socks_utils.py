import socket

def create_tcp_server_socket(address, port, queue_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((address, port))
    sock.listen(queue_size)
    return sock


def create_tcp_client_socket(address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock


def receive_all(socket, length):
    try:
        msg = socket.recv(length)
        return msg
    except socket.error:
        print "erro"
