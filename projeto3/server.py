from flask import Flask, request, make_response, g
import sqlite3, json
from createBD import connect_db

app = Flask(__name__)

DATABASE = "proj.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/utilizadores', methods = ["GET", "POST", "DELETE", "PUT"])
@app.route('/utilizadores/<int:id>', methods = ["GET", "DELETE"])

def utilizadores(id = None):
    conn, cursor = (g.db, g.db.cursor())

    if request.method == "GET": #buscar user
        if id == None:
            get_user_query = cursor.execute("SELECT * FROM users")
        else:
            get_user_query = cursor.execute("SELECT * FROM users WHERE id = ?", (id, ))

        user_result = cursor.fetchall()

        if len(user_result) > 0:
            r = make_response(json.dumps(user_result))
            r.status_code = 200
        else:
            r = make_response(json.dumps("Nenhum utilizador encontrado"))
            r.status_code = 404


    elif request.method == "POST": #adiciona user
        user = json.loads(request.data)
        user_to_insert = (user["name"], user["username"], user["password"])

        insert_user_query = cursor.execute("INSERT INTO users (name, username, password) VALUES (?, ?, ?)", user_to_insert)
        conn.commit()

        get_id_query = cursor.execute("SELECT id FROM users WHERE name = ? AND username = ? AND password = ?", user_to_insert)
        id_user = cursor.fetchone()[0]

        r = make_response(json.dumps("utilizador inserido"))
        r.headers['location'] = '/utilizadores/' + str(id_user)
        r.status_code = 200

    elif request.method == "DELETE": #delete user
        get_user_query = cursor.execute("SELECT * FROM users")
        user_result = cursor.fetchall()

        if len(user_result) > 0:
            if id == None:
                delete_user_query = cursor.execute("DELETE FROM users")
                conn.commit()

            else:
                delete_user_query = cursor.execute("DELETE FROM users WHERE id = ?", (id, ))
                conn.commit()

            r = make_response(json.dumps("Utilizador removido"))
            r.status_code = 200

        else:
            r = make_response(json.dumps("Nenhum utilizador encontrado"))
            r.status_code = 404

    if request.method == "PUT": #update user
        user = json.loads(request.data)
        user_to_update = (user["password"], user["user"])

        get_user_query = cursor.execute("SELECT * FROM users WHERE id = ?", (user["user"], ))

        user_result = cursor.fetchall()

        if len(user_result) > 0:
            update_user_query = cursor.execute("UPDATE users SET password = ? WHERE id = ?", user_to_update)
            conn.commit()

            r = make_response(json.dumps("Utilizador modificado"))
            r.status_code = 200

        else:
            r = make_response(json.dumps("Utilizador nao encontrado"))
            r.status_code = 200

    conn.close()
    return r


@app.route('/series', methods = ["GET", "POST", "DELETE", "PUT"])
@app.route('/series/<int:id>', methods = ["GET", "DELETE"])
@app.route('/series/<rate>', methods = ["POST"])

def series(id = None, rate = None):
    conn, cursor = (g.db, g.db.cursor())

    if request.method == "GET": #buscar serie
        if request.data:
            data = json.loads(request.data)

            if data.keys()[0] == "user":
                get_user_serie_query = cursor.execute("SELECT * FROM list_series WHERE user_id = ?", (data["user"], ))

                user_serie_result = cursor.fetchall()

                if len(user_serie_result) > 0:
                    r = make_response(json.dumps(user_serie_result))
                    r.status_code = 200

                else:
                    r = make_response(json.dumps("Utilizador sem series"))
                    r.status_code = 404

            if data.keys()[0] == "category":
                get_category_serie_query = cursor.execute("SELECT * FROM serie WHERE category_id = ?", (data["category"], ))

                category_serie_result = cursor.fetchall()

                if len(category_serie_result) > 0:
                    r = make_response(json.dumps(category_serie_result))
                    r.status_code = 200

                else:
                    r = make_response(json.dumps("Categoria sem series"))
                    r.status_code = 404

        else:
            if id == None:
                get_serie_query = cursor.execute("SELECT * FROM serie")
            else:
                get_serie_query = cursor.execute("SELECT * FROM serie WHERE id=?", (id, ))

            serie_result = cursor.fetchall()

            if len(serie_result) > 0:
                r = make_response(json.dumps(serie_result))
                r.status_code = 200
            else:
                r = make_response(json.dumps("Nenhuma serie encontrada"))
                r.status_code = 404

    elif request.method == "POST":
        if rate == None: #adiciona serie
            serie = json.loads(request.data)

            serie_to_insert = (serie["series_name"], serie["date"], serie["synopse"], serie["category"])

            try:
                insert_serie_query = cursor.execute("INSERT INTO serie (name, start_date, synopse, category_id) VALUES (?, ?, ?, ?)", serie_to_insert)
                conn.commit()

                get_id_query = cursor.execute("SELECT id FROM serie WHERE name = ? AND start_date = ? AND synopse = ? AND category_id = ?", serie_to_insert)
                id_serie = cursor.fetchone()[0]
                r = make_response(json.dumps("Serie Inserted"))
                r.headers['location'] = '/series/' + str(id_serie)
                r.status_code = 200

            except sqlite3.IntegrityError:
                r = make_response(json.dumps("Categoria nao existe"))
                r.status_code = 404


        else: #adiciona classification
            user_rate = json.loads(request.data)

            get_user_query = cursor.execute("SELECT * FROM users WHERE id = ?", (int(user_rate["user"]), ))

            user_result = cursor.fetchall()

            if len(user_result) > 0:
                get_serie_query = cursor.execute("SELECT * FROM serie WHERE id = ?", (int(user_rate["serie"]), ))

                serie_result = cursor.fetchall()

                if len(serie_result) > 0:
                    get_rating_query = cursor.execute("SELECT * FROM classification WHERE initials = ?", (user_rate["classification"], ))
                    rating_result = cursor.fetchone()

                    if len(rating_result) > 0:
                        rate_to_insert = (user_rate["user"], rating_result[0], user_rate["serie"])

                        try:
                            insert_rating_query = cursor.execute("INSERT INTO list_series VALUES (?, ?, ?)", rate_to_insert)
                            conn.commit()

                            r = make_response(json.dumps("Rating inserido"))
                            r.headers['location'] = '/series/' + user_rate["classification"]
                            r.status_code = 200

                        except sqlite3.IntegrityError:
                            r = make_response(json.dumps("Utilizador ja classificou serie"))
                            r.status_code = 405


                    else:
                        r = make_response(json.dumps("Classificacao nao existe"))
                        r.status_code = 404

                else:
                    r = make_response(json.dumps("Serie nao existe"))
                    r.status_code = 404

            else:
                r = make_response(json.dumps("Utilizador nao existe"))
                r.status_code = 404

    elif request.method == "DELETE": #remove serie
        if request.data:
            data = json.loads(request.data)

            if data.keys()[0] == "user":
                get_user_serie_query = cursor.execute("SELECT * FROM list_series WHERE user_id = ?", (data["user"], ))

                user_serie_result = cursor.fetchall()

                if len(user_serie_result) > 0:
                    get_user_serie_query = cursor.execute("DELETE FROM list_series WHERE user_id = ?", (data["user"], ))
                    conn.commit()

                    r = make_response(json.dumps("Apagada serie do User"))
                    r.status_code = 200

                else:
                    r = make_response(json.dumps("Utilizador sem series"))
                    r.status_code = 404


            elif data.keys()[0] == "category":
                get_category_serie_query = cursor.execute("SELECT * FROM serie WHERE category_id = ?", (data["category"], ))

                category_serie_result = cursor.fetchall()

                if len(category_serie_result) > 0:
                    get_category_serie_query = cursor.execute("DELETE FROM serie WHERE category_id = ?", (data["category"], ))
                    conn.commit()

                    r = make_response(json.dumps("Apagada serie da Categoria"))
                    r.status_code = 200

                else:
                    r = make_response(json.dumps("Categoria sem series"))
                    r.status_code = 404


        else:
            get_serie_query = cursor.execute("SELECT * FROM serie")
            serie_result = cursor.fetchall()

            if len(serie_result) > 0:
                if id == None:
                    delete_serie_query = cursor.execute("DELETE FROM serie")
                    conn.commit()

                else:
                    delete_serie_query = cursor.execute("DELETE FROM serie WHERE id = ?", (id, ))
                    conn.commit()

                r = make_response(json.dumps("Serie apagada"))
                r.status_code = 200

            else:
                r = make_response(json.dumps("Nenhuma serie encontrada"))
                r.status_code = 404

    elif request.method == "PUT": #update classificacao
        user_rate = json.loads(request.data)

        get_user_rate_query = cursor.execute("SELECT * FROM list_series WHERE user_id = ? AND serie_id = ?", (user_rate["user"], user_rate["serie"]))

        user_rate_result = cursor.fetchall()

        if len(user_rate_result) > 0:
            get_rating_query = cursor.execute("SELECT * FROM classification WHERE initials = ?", (user_rate["classification"], ))
            rating_result = cursor.fetchone()

            if len(rating_result) > 0:
                rating_to_update = (rating_result[0], user_rate["user"], user_rate["serie"])
                update_rating_query = cursor.execute("UPDATE list_series SET classification_id = ? WHERE user_id = ? AND serie_id = ?", rating_to_update)
                conn.commit()

                r = make_response(json.dumps("Classificacao modificada"))
                r.status_code = 200

            else:
                r = make_response(json.dumps("Classificacao nao existe"))
                r.status_code = 404

        else:
            r = make_response(json.dumps("Utilizador sem series"))
            r.status_code = 404

    conn.close()
    return r


@app.route('/episodios', methods = ["GET", "POST", "DELETE"])
@app.route('/episodios/<int:id>', methods = ["GET", "DELETE"])

def episodes(id = None):
    conn, cursor = (g.db, g.db.cursor())

    if request.method == "GET": #buscar episodio
        if id == None:
            get_episode_query = cursor.execute("SELECT * FROM episode")
        else:
            get_episode_query = cursor.execute("SELECT * FROM episode WHERE id=?",(id, ))

        episode_result = cursor.fetchall()

        if len(episode_result) > 0:
            r = make_response(json.dumps(episode_result))
            r.status_code = 200

        else:
            r = make_response(json.dumps("Nenhum episodio encontrado"))
            r.status_code = 404

    elif request.method == "POST": #adiciona episodio
        episode = json.loads(request.data)
        episode_to_insert = (episode["episode_name"], episode["description"], episode["serie"])

        try:
            insert_episode_query = cursor.execute("INSERT INTO episode (name, description, serie_id) VALUES (?, ?, ?)", episode_to_insert)
            conn.commit()

            get_id_query = cursor.execute("SELECT id FROM episode WHERE name = ? AND description = ? AND serie_id = ? ", episode_to_insert)
            id_episode = cursor.fetchone()[0]
            r = make_response(json.dumps("Episode Inserted"))
            r.headers['location'] = '/episodios/' + str(id_episode)

        except sqlite3.IntegrityError:
            r = make_response(json.dumps("Serie nao existe"))
            r.status_code = 404


    elif request.method == "DELETE": #remove episodio
        get_episodio_query = cursor.execute("SELECT * FROM episode")
        episodio_result = cursor.fetchall()

        if len(episodio_result) > 0:
            if id == None:
                delete_episodio_query = cursor.execute("DELETE FROM episode")
                conn.commit()
            else:
                delete_episodio_query = cursor.execute("DELETE FROM episode WHERE id = ?", (id, ))
                conn.commit()

            r = make_response(json.dumps("Episodio apagada"))
            r.status_code = 200

        else:
            r = make_response(json.dumps("Nenhum episodio encontrada"))
            r.status_code = 404

    conn.close()
    return r


if __name__ == '__main__':
    conn, cursor = connect_db('proj.db')
    app.run(debug = True)
