import sqlite3
from os.path import isfile

classifications = [(1, 'M', 'MAU'),
                   (2, 'MM', 'Mais ou menos'),
                   (3, 'S', 'Suficiente'),
                   (4, 'B', 'Bom'),
                   (5, 'MB', 'Muito bom')]

categories = [(1, 'Acao', 'Acao'),
              (2, 'Animacao', 'Animacao'),
              (3, 'Artes Marciais', 'Artes Marciais'),
              (4, 'Aventura', 'Aventura'),
              (5, 'Biografia', 'Biografia'),
              (6, 'Classico', 'Classico'),
              (7, 'Comedia', 'Comedia'),
              (8, 'Drama', 'Drama'),
              (9, 'Ficcao cientifica', 'Ficcao cientifica'),
              (10, 'Musical', 'Musical'),
              (11, 'Policial', 'Policial'),
              (12, 'Romance', 'Romance'),
              (13, 'Suspense', 'Suspense'),
              (15, 'Terror', 'Terror')]

def connect_db(dbname):
    db_is_created = isfile(dbname)
    connection = sqlite3.connect('proj.db')
    cursor = connection.cursor()
    connection.execute("PRAGMA foreign_keys = ON;")
    if not db_is_created:
        cursor.execute('''CREATE TABLE users (
                          id INTEGER PRIMARY KEY,
                          name VARCHAR(128),
                          username VARCHAR(64),
                          password VARCHAR(64)
                          );''')

        cursor.execute('''CREATE TABLE classification (
                          id INTEGER PRIMARY KEY,
                          initials VARCHAR(10),
                          description TEXT
                          );''')

        cursor.execute('''CREATE TABLE category (
                          id INTEGER PRIMARY KEY,
                          name VARCHAR(20),
                          description TEXT
                          );''')

        cursor.execute('''CREATE TABLE list_series (
                          user_id INTEGER,
                          classification_id INTEGER,
                          serie_id INTEGER,
                          PRIMARY KEY (user_id, serie_id),
                          FOREIGN KEY(user_id) REFERENCES users(id),
                          FOREIGN KEY(classification_id) REFERENCES classification(id),
                          FOREIGN KEY(serie_id) REFERENCES serie(id)
                          );''')

        cursor.execute('''CREATE TABLE serie (
                          id INTEGER PRIMARY KEY,
                          name VARCHAR(20),
                          start_date DATE,
                          synopse TEXT,
                          category_id INTEGER,
                          FOREIGN KEY(category_id) REFERENCES category(id)
                          );''')

        cursor.execute('''CREATE TABLE episode (
                          id INTEGER PRIMARY KEY,
                          name TEXT,
                          description TEXT,
                          serie_id INTEGER,
                          FOREIGN KEY(serie_id) REFERENCES serie(id)
                          );''')

        cursor.executemany('INSERT INTO classification VALUES (?, ?, ?)', classifications)

        cursor.executemany('INSERT INTO category VALUES (?, ?, ?)', categories)
        connection.commit()

    return connection, cursor

if __name__ == '__main__':
    conn, cursor = connect_db('proj.db')
    conn.close()
