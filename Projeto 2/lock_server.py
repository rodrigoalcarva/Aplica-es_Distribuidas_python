#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_server.py
Grupo: 038
Números de aluno: 50002,50011,50035
"""

# Zona para fazer importação

import time, sys, pickle, struct
from socks_utils import create_tcp_server_socket, receive_all
from lock_skel import *
import select

Host = ''
Port = int(sys.argv[1])

print "Host:" + "127.0.0.1"
print "Port:" + str(Port)

numberRecurses = sys.argv[2]         
numberMaxBlocks = sys.argv[3]
numberBlocksSameTime = sys.argv[4]
maxTime = sys.argv[5]

resource_pool = Skeleton(numberRecurses, numberMaxBlocks, numberBlocksSameTime, maxTime)

sock = create_tcp_server_socket(Host, Port, 1)

SocketList = [sock]
currentClients = []
#try:
while True:
    R, W, X = select.select(SocketList, [], [])

    for sk in R:
        if sk is sock:
            (conn_sock, addr) = sock.accept()

            ID = receive_all(conn_sock, 4)
        
            if ID not in currentClients:                      
                addr, port = conn_sock.getpeername()
                print 'Novo cliente ligado desde ' + str(addr) + ' ' + str(port)
                SocketList.append(conn_sock)
                currentClients.append(ID)

                msg_bytes = pickle.dumps('OK', -1)
                size_bytes = struct.pack('!i', len(msg_bytes))

                conn_sock.sendall(size_bytes)
                conn_sock.sendall(msg_bytes)

                
            else:
                msg_bytes = pickle.dumps('NOK', -1)
                size_bytes = struct.pack('!i', len(msg_bytes))

                conn_sock.sendall(size_bytes)
                conn_sock.sendall(msg_bytes)

                conn_sock.close()
        else:
            msg = receive_all(sk, 4)
            
            if msg:  
                asw = resource_pool.processAsw(msg)

                if asw[0] == "EXIT":
                    sk.close()
                    SocketList.remove(sk)
                    print asw[1]
                    currentClients.remove(asw[1])

                elif asw == "UNKNOWN COMMAND":
                    msg_bytes = pickle.dumps('UNKNOWN COMMAND', -1)
                    size_bytes = struct.pack('!i', len(msg_bytes))

                    sk.sendall(size_bytes)
                    sk.sendall(msg_bytes)
                    
                else:
                    msg_bytes = pickle.dumps(asw, -1)
                    size_bytes = struct.pack('!i', len(msg_bytes))

                    sk.sendall(size_bytes)
                    sk.sendall(msg_bytes)

            else:
                sk.close()
                SocketList.remove(sk)
                currentClients.remove(ID)
                print currentClients

#except:
    #print "Servidor fechado"
   # sock.close()

sock.close()
