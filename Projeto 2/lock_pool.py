"""
Aplicações distribuídas - Projeto 1 - lock_client.py
Grupo: 038
Números de aluno: 50002, 50011, 50035
"""


import time

class resource_lock:
    def __init__(self):
        """
        Define e inicializa as características de um LOCK num recurso.
        """
        self.locked = False         #Bloqueado ou não
        self.active = True
        self.locked_count = 0       #Vezes bloqueado
        self.current_client = None  #Cliente a usar
        self.locked_time = 0
        self.k = 0
        self.y = 0

        self.endTime = time.time()
        self.wait_line = []

    def lock(self, client_id, time_limit):
        """
        Bloqueia o recurso se este não estiver bloqueado ou inativo, ou mantém o bloqueio
        se o recurso estiver bloqueado pelo cliente client_id. Neste caso renova
        o bloqueio do recurso até time_limit.
        Retorna True se bloqueou o recurso ou False caso contrário.
        """
        if self.locked_count < self.k:
            if self.active:
                if self.locked:
                    if self.current_client == client_id:
                        self.locked_count += 1
                        self.locked_time = time.time() + time_limit
                        
                    else:
                        self.wait_line.append(client_id)
                        self.locked_count += 1

                    return False
                
                else:
                    self.locked = True
                    self.current_client = client_id
                    self.locked_time = time.time()
                    self.locked_count += 1
                    return True
                
        else:
            self.locked = False
            self.disable()
                
        return False

    def urelease(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        if len(self.wait_line) > 0:
            self.current_client = self.wait_line.pop(0)
            self.locked_time = time.time()

        else:
            self.locked = False
            self.client_id = None

    def release(self, client_id):
        """
        Liberta o recurso se este foi bloqueado pelo cliente client_id,
        retornando True nesse caso. Caso contrário retorna False.
        """
        if self.current_client == client_id:
            self.urelease()
            return True
        
        elif client_id in self.wait_line:
            self.wait_line.remove(client_id)
            return True


        return False

    def test(self):
        """
        Retorna o estado de bloqueio do recurso ou inativo, caso o recurso se
        encontre inativo.
        """
        if self.active:
            return self.locked

        return "inactive"

    def stat(self):
        """
        Retorna o número de vezes que este recurso já foi bloqueado em k.
        """
        return self.locked_count

    def disable(self):
        """
        Coloca o recurso inativo/indisponível incondicionalmente, alterando os
        valores associados à sua disponibilidade.
        """
        self.active = False


class lock_pool:
    def __init__(self, N, K, Y, T):
        """
        Define um array com um conjunto de locks para N recursos. Os locks podem
        ser manipulados pelos métodos desta classe.
        Define K, o número máximo de bloqueios permitidos para cada recurso. Ao
        atingir K, o recurso fica indisponível/inativo.
        Define Y, o número máximo permitido de recursos bloqueados num dado
        momento. Ao atingir Y, não é possível realizar mais bloqueios até que um
        recurso seja libertado.
	Define T, o tempo máximo de concessão de bloqueio.
        """
        self.lock_array = []

        self.k = int(K)
        self.y = int(Y)
        self.t = int(T)

        for i in range(int(N)):
            newResource = resource_lock()
            newResource.k = self.k
            newResource.y = self.y
            self.lock_array.append(newResource)


    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão do bloqueio. Liberta os recursos caso o seu tempo de
        concessão tenha expirado.
        """
        for el in self.lock_array:
            if el.locked:
                if time.time() - el.locked_time > self.t:
                    el.urelease()


    def lock(self, resource_id, client_id, time_limit):
        """
        Tenta bloquear o recurso resource_id pelo cliente client_id, até ao
        instante time_limit.
        O bloqueio do recurso só é possível se o recurso estiver ativo, não
        bloqueado ou bloqueado para o próprio requerente, e Y ainda não foi
        excedido. É aconselhável implementar um método __try_lock__ para
        verificar estas condições.
        Retorna True em caso de sucesso e False caso contrário.
        """
        res = self.lock_array[resource_id]
        
        if self._try_lock_(resource_id, client_id):
            if res.lock(client_id, time_limit):
                return True

        return False


    def _try_lock_(self, resource_id,client_id):
        """
        """
        current_lock = []

        for i in range(len(self.lock_array)):
            if self.lock_array[i].locked:
                current_lock.append(i)
                
        res = self.lock_array[resource_id]

        if res.active:
            
            if not res.locked or (res.locked and client_id != res.current_client):
                if resource_id in current_lock or (resource_id not in current_lock and len(current_lock) < res.y):
                    return True


        return False
                        
    
    def release(self, resource_id, client_id):
        """
        Liberta o bloqueio sobre o recurso resource_id pelo cliente client_id.
        True em caso de sucesso e False caso contrário.
        """
        return self.lock_array[resource_id].release(client_id)

    def test(self,resource_id):
        """
        Retorna True se o recurso resource_id estiver bloqueado e False caso
        esteja bloqueado ou inativo.
        """
        return self.lock_array[resource_id].test()


    def stat(self,resource_id):
        """
        Retorna o número de vezes que o recurso resource_id já foi bloqueado, dos
        K bloqueios permitidos.
        """
        return self.lock_array[resource_id].stat()
        

    def stat_y(self):
        """
        Retorna o número de recursos bloqueados num dado momento do Y permitidos.
        """
        current_lock = 0

        for el in self.lock_array:
            if el.active and el.locked:
                current_lock += 1

        return current_lock

    def stat_n(self):
        """
        Retorna o número de recursos disponíneis em N.
        """
        current_active = 0

        for el in self.lock_array:
            if el.active and not el.locked:
                current_active += 1

        return current_active

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print.
        """
        output = ""

        for i in range(len(self.lock_array)):
            if self.lock_array[i].active:
                if self.lock_array[i].locked:
                    if self.lock_array[i].endTime <= time.time():
                        self.lock_array[i].endTime = time.time() + self.t
                        
                    output += "recurso <" + str(i+1) +"> bloqueio pelo cliente <" + str(self.lock_array[i].current_client) + "> ate <" + time.ctime(self.lock_array[i].endTime) + "> \n" 
                else:
                    output += "recurso <" + str(i+1) +"> desbloqueado \n"
            else:
                output += "recurso <" + str(i+1) + "> inativo \n"
        
        #
        # Acrescentar na output uma linha por cada recurso bloqueado, da forma:
        # recurso <número do recurso> bloqueado pelo cliente <id do cliente> até
        # <instante limite da concessão do bloqueio>
        #
        # Caso o recurso não esteja bloqueado a linha é simplesmente da forma:
        # recurso <número do recurso> desbloqueado
        # Caso o recurso esteja inativo a linha é simplesmente da forma:
        # recurso <número do recurso> inativo
        #
        return output
