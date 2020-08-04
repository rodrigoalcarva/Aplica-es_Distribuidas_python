"""
Aplicações distribuídas - Projeto 1 - lock_server.py
Grupo: 038
Números de aluno: 50002,50011,50035
"""

from net_client import *

class Stub:
    def __init__(self, host, port, ID):
        self.client = server(host, port)
        self.ID = ID
        
    def connect(self):
        self.client.connect()

    def send_receive(self, com):
        comandsDict = {"LOCK": 10, "RELEASE": 20,"TEST": 30,"STATS": 40,"STATS-Y": 50,"STATS-N": 60}
        msg = []

        if com == self.ID:
            msg = com

        elif len(com) == 2:
            if com[0] == "STATS" or com[0] == "TEST":
                msg = [comandsDict[com[0]], int(com[1])]
            elif com[0] == "LOCK" or com[0] == "RELEASE":
                msg = [comandsDict[com[0]], int(self.ID), int(com[1])]
            else:
                msg = "UNKNOWN COMMAND"

        elif len(com) == 1:
            if com[0] == "STATS-N" or com[0] == "STATS-Y":
                msg = [comandsDict[com[0]]]
            else:
                msg = "UNKNOWN COMMAND"

        else:
            msg = "UNKNOWN COMMAND"

        return self.client.send_receive(msg)
        

    def close(self, IDClient):
        msg_bytes = pickle.dumps(['EXIT', IDClient], -1)
        size_bytes = struct.pack('!i', len(msg_bytes))

        self.client.sock.sendall(size_bytes)
        self.client.sock.sendall(msg_bytes)
