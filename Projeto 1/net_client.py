# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - net_client.py
Grupo:
Números de aluno:
"""

# zona para fazer importação

from socks_utils import create_tcp_client_socket
import pickle, struct

# definição da classe server 

class server:
    """
    Classe para abstrair uma ligação a um servidor TCP. Implementa métodos
    para estabelecer a ligação, para envio de um comando e receção da resposta,
    e para terminar a ligação
    """
    def __init__(self, address, port):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        self.address = address
        self.port = port
        self.sock = None        
        
    def connect(self):
        """
        Estabelece a ligação ao servidor especificado na inicialização do
        objeto.
        """
        self.sock = create_tcp_client_socket(self.address, self.port)
        self.sock.connect((self.address, self.port))
        
    def send_receive(self, data):
        """
        Envia os dados contidos em data para a socket da ligação, e retorna a
        resposta recebida pela mesma socket.
        """
        msg_bytes = pickle.dumps(data, -1)
        size_bytes = struct.pack('!i', len(msg_bytes))

        self.sock.sendall(size_bytes)
        self.sock.sendall(msg_bytes)
        
        resposta = self.sock.recv(1024)
        return resposta
    
    def close(self):
        """
        Termina a ligação ao servidor.
        """
        self.sock.close()
