import sys, requests, json

com = ""
showRes = True

try:
    while com != "EXIT":
        com = raw_input("Insira o comando: ").split(" ")

        operation = com[0]

        if operation == "ADD":
            if com[1] == "USER":
                user = {"name": com[2], "username": com[3], "password": com[4]}
                r = requests.post('http://localhost:5000/utilizadores', json = user)

            if com[1] == "SERIE":
                serie = {"series_name": com[2], "date": com[3], "synopse": com[4],"category": com[5]}
                r = requests.post('http://localhost:5000/series', json = serie)

            if com[1] == "EPISODIO":
                episode = {"episode_name": com[2], "description": com[3], "serie": com[4]}
                r = requests.post('http://localhost:5000/episodios', json = episode)

            elif len(com) == 4:
                rate = {"user": com[1], "serie": com[2], "classification": com[3]}
                r = requests.post('http://localhost:5000/series/%s' %str(com[3]), json = rate)


        elif operation == "REMOVE" or operation == "SHOW":
            if com[1] == "USER":
                if operation == "REMOVE":
                    r = requests.delete('http://localhost:5000/utilizadores/%s' %(str(com[2])))

                elif operation == "SHOW":
                    r = requests.get('http://localhost:5000/utilizadores/%s' %(str(com[2])))

            if com[1] == "SERIE":
                if operation == "REMOVE":
                    r = requests.delete('http://localhost:5000/series/%s' %(str(com[2])))

                elif operation == "SHOW":
                    r = requests.get('http://localhost:5000/series/%s' %(str(com[2])))

            if com[1] == "EPISODIO":
                if operation == "REMOVE":
                    r = requests.delete('http://localhost:5000/episodios/%s' %(str(com[2])))

                elif operation == "SHOW":
                    r = requests.get('http://localhost:5000/episodios/%s' %(str(com[2])))

            elif com[1] == "ALL":
                if com[2] == "SERIE_U":
                    user = {"user": com[3]}
                    if operation == "REMOVE":
                        r = requests.delete('http://localhost:5000/series',json = user)

                    elif operation == "SHOW":
                        r = requests.get('http://localhost:5000/series',json = user)


                if com[2] == "SERIE_C":
                    category = {"category": com[3]}
                    if operation == "REMOVE":
                        r = requests.delete('http://localhost:5000/series',json = category)

                    elif operation == "SHOW":
                        r = requests.get('http://localhost:5000/series',json = category)


                if com[2] == "EPISODIO" and len(com) == 4:
                    serie = {"serie": com[3]}
                    if operation == "REMOVE":
                        r = requests.delete('http://localhost:5000/episodios',json = serie)

                    elif operation == "SHOW":
                        r = requests.get('http://localhost:5000/episodios',json = serie)


                elif len(com) == 3:
                    if com[2] == "USERS":
                        if operation == "REMOVE":
                            r = requests.delete('http://localhost:5000/utilizadores')
                        elif operation == "SHOW":
                            r = requests.get('http://localhost:5000/utilizadores')

                    elif com[2] == "SERIE":
                        if operation == "REMOVE":
                            r = requests.delete('http://localhost:5000/series')
                        elif operation == "SHOW":
                            r = requests.get('http://localhost:5000/series')

                    elif com[2] == "EPISODIO":
                        if operation == "REMOVE":
                            r = requests.delete('http://localhost:5000/episodios')
                        elif operation == "SHOW":
                            r = requests.get('http://localhost:5000/episodios') 


        elif operation == "UPDATE":
            if com[1] == "SERIE":
                rate = {"user": com[2], "serie": com[3], "classification": com[4]}
                r = requests.put('http://localhost:5000/series', json = rate)

            elif com[1] == "USER":
                user = {"user": com[2], "password": com[3]}
                r = requests.put('http://localhost:5000/utilizadores', json = user)

        elif operation == "EXIT":
            com = "EXIT"
            showRes = False

        else:
            print "Comando nao reconhecido"
            showRes = False

        if showRes:
            asw = json.loads(r.content)

            if isinstance(asw, list):
                for el in asw:
                    print el
            else:
                print asw

            print r.status_code
            print r.headers
            print "****"

except requests.exceptions.ConnectionError:
    print "Servidor desativo"
    showRes = False
