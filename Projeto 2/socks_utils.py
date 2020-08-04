"""
Aplicações distribuídas - Projeto 1 - net_client.py
Grupo: 038
Números de aluno: 50002, 50011,50035
"""

import socket
import struct, pickle

def create_tcp_server_socket(address, port, queue_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((address, port))
    sock.listen(queue_size)
    return sock


def create_tcp_client_socket(address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock


def receive_all(socket, length):
    #try:

    size_bytes = ''
    while len(size_bytes) < length:
        pacote = socket.recv(length - len(size_bytes))
        if pacote:
            size_bytes += pacote

    
    size = struct.unpack('!i', size_bytes)[0]
    msg_bytes = socket.recv(size)
    msg = pickle.loads(msg_bytes)
    return msg
    
    #except:
     #   print "erro"
