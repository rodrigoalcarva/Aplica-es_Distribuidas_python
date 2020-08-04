#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_client.py
Grupo: 038
Números de aluno: 50002, 50011, 50035
"""
# Zona para fazer imports

from lock_stub import *
import sys

# Programa principal

args = sys.argv

Host = args[1]
Port = int(args[2])
IDClient = args[3]

try:
    clientStub = Stub(Host, Port, IDClient)

    clientStub.connect()
except:
    print "Erro ao conectar"
    sys.exit()

sendID = clientStub.send_receive(IDClient)

if sendID != "OK":
    print "ID ja se encontra sobre uso"

else:
    try:
        cont = True
        while cont:    
            com = raw_input("Comando > ").split(" ")

            if com[0] == "EXIT":
                cont = False
            
            else:
                answer_serv = clientStub.send_receive(com)

                print answer_serv

        clientStub.close(IDClient)
    except:
        print "Socket Fechado"
    
        
    
