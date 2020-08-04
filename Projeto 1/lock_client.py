#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_client.py
Grupo:
Números de aluno:
"""
# Zona para fazer imports

from net_client import *
import sys

# Programa principal

args = sys.argv

Host = args[1]
Port = int(args[2])

client = server(Host, Port)

res =''
while True:
    com = raw_input("Comando > ")

    if com.split(" ")[0] == "EXIT":
        exit()

    else:
        client.connect()
       
        answer_serv = client.send_receive(com)

        print answer_serv
        
        client.close()
