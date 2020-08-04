"""
Aplicações distribuídas - Projeto 1 - lock_server.py
Grupo: 038
Números de aluno: 50002,50011,50035
"""

from lock_pool import *

class Skeleton:
    def __init__(self, numRecursos, numMaxBlocks, numBlocksSameTime, maxTime):
        self.resources = lock_pool(numRecursos, numMaxBlocks, numBlocksSameTime, maxTime)       

    def processAsw(self, msg):
        asw = ""
        self.resources.clear_expired_locks()                    

        if msg[0] == "EXIT":
            asw = msg

        elif msg == "UNKNOWN COMMAND":
            asw = "UNKNOWN COMMAND"
        
        elif len(msg)==1 or (len(msg) == 2 and msg[1]-1 < len(self.resources.lock_array)) or (len(msg) == 3 and msg[2]-1 < len(self.resources.lock_array)):
            if int(msg[0]) == 10:
                if self.resources.lock(msg[2]-1, msg[1], self.resources.t):
                    asw = [msg[0] +1, True]
                else:
                    asw = [msg[0] +1, False]
                        
            elif int(msg[0]) == 20:
                if self.resources.release(msg[2]-1, msg[1]):
                    asw = [msg[0] +1, True]
                else:
                    asw = [msg[0] +1, False]
                    
                    
            elif int(msg[0]) == 30:
                if self.resources.test(msg[1]-1) == "inactive":
                    asw = [msg[0] +1, None]
                else:
                    if self.resources.test(msg[1]-1):
                        asw = [msg[0] +1, True]
                    else:
                        asw = [msg[0] +1, False]
                
            elif int(msg[0]) == 40:
                asw = [msg[0] +1, self.resources.stat(msg[1]-1)]
                
            elif int(msg[0]) == 50:
                asw = str(self.resources.stat_y())
                 
            elif int(msg[0]) == 60:
                asw = str(self.resources.stat_n())                   

        else:
            print msg
            print self.resources.k
            asw = [int(msg[0]) +1, None]

        print self.resources

        return asw
        
