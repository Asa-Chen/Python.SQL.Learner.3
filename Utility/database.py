import sqlite3
CREATE_MOVIE_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title,
    release_date)"""
CREATE_USER_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
    )"""
CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_name,
    movie_id INTEGER,
    FOREIGN KEY(user_name) REFERENCES users(username),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
    )"""
INSERT_MOVIES = "INSERT INTO movies (title, release_date) VALUES (?, ?)"
INSERT_WATCHED = "INSERT INTO watched (user_name, movie_id) VALUES (?, ?)"
INSERT_USER = "INSERT INTO users (username) VALUES (?)"
DELETE_MOVIES = "DELETE FROM movies WHERE title=?"
SELECT_ALL_MOVIES = "SELECT * FROM movies"
SELECT_WATCHED_NEW = """SELECT movies.*
    FROM movies
    JOIN watched ON watched.movie_id = movies.id
    JOIN users ON users.username = watched.user_name
    WHERE users.username=?"""
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_date > ?"
SEARCH_MOVIES = "SELECT * FROM movies WHERE title LIKE ?"

connection = sqlite3.connect('data.db')

def create_table():
    with connection:
        connection.execute(CREATE_MOVIE_TABLE)
        connection.execute(CREATE_WATCHED_TABLE)
        connection.execute(CREATE_USER_TABLE)

def add_movie(title, release_date):
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_date,))

def add_user(user):
    with connection:
        connection.execute(INSERT_USER, (user,))

def delete_movie(title):
    with connection:
        connection.execute(DELETE_MOVIES, (title,))

def select_movies(): #returns a list of tuples
    with connection:
        return connection.execute(SELECT_ALL_MOVIES).fetchall()

def select_upcoming(date):
    with connection:
        return connection.execute(SELECT_UPCOMING_MOVIES, (date,)).fetchall()

def select_watched(user): #returns a list of tuples
    with connection:
        return connection.execute(SELECT_WATCHED_NEW, (user,)).fetchall()

def search_movies(target):
    with connection:
        return connection.execute(SEARCH_MOVIES, (f"%{target}%", )).fetchall()

def mark_movie(user, movie_id):
    with connection:
        connection.execute(INSERT_WATCHED, (user, movie_id,))

def check_movie_presense(movie_id):
    with connection: #bool of a list returned by a cursor.fetchall() from connection
        return bool(connection.execute("SELECT * FROM movies WHERE id=?", (movie_id,)).fetchall())

def check_user_presense(user_id):
    with connection:
        return bool(connection.execute("SELECT * FROM users WHERE username=?", (user_id,)).fetchall())

