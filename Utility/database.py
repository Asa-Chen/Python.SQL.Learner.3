import os
import psycopg2
from dotenv import load_dotenv
load_dotenv() #When left empty, it will try and load the .env in the main directory, meaning you can use DATABASE_URL f
#from .env
CREATE_MOVIE_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    release_date DATE);"""
CREATE_USER_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
    );"""
CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_name TEXT,
    movie_id INTEGER,
    FOREIGN KEY(user_name) REFERENCES users(username),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
    );"""
INSERT_MOVIES = "INSERT INTO movies (title, release_date) VALUES (%s, %s);"
INSERT_WATCHED = "INSERT INTO watched (user_name, movie_id) VALUES (%s, %s);"
INSERT_USER = "INSERT INTO users (username) VALUES (%s);"
DELETE_MOVIES = "DELETE FROM movies WHERE title=%s;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_WATCHED_NEW = """SELECT movies.*
    FROM movies
    JOIN watched ON watched.movie_id = movies.id
    JOIN users ON users.username = watched.user_name
    WHERE users.username=%s;"""
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_date > %s;"
SEARCH_MOVIES = "SELECT * FROM movies WHERE title LIKE %s;"

connection = psycopg2.connect(os.environ["DATABASE_URL"]) #os is a standard package, environ is a dictionary
#psycopg2 also requires cursors
def create_table(): #PostgreSQL requires a cursor
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIE_TABLE)
            cursor.execute(CREATE_USER_TABLE)
            cursor.execute(CREATE_WATCHED_TABLE)


def add_movie(title, release_date):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIES, (title, release_date,))

def add_user(user):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (user,))

def delete_movie(title):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_MOVIES, (title,))

def select_movies(): #returns a list of tuples
    with connection:
        with connection.cursor() as cursor:
            return cursor.execute(SELECT_ALL_MOVIES).fetchall()

def select_upcoming(date):
    with connection:
        with connection.cursor() as cursor:
            return cursor.execute(SELECT_UPCOMING_MOVIES, (date,)).fetchall()

def select_watched(user): #returns a list of tuples
    with connection:
        with connection.cursor() as cursor:
            return cursor.execute(SELECT_WATCHED_NEW, (user,)).fetchall()

def search_movies(target):
    with connection:
        with connection.cursor() as cursor:
            return cursor.execute(SEARCH_MOVIES, (f"%{target}%", )).fetchall()

def mark_movie(user, movie_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_WATCHED, (user, movie_id,))

def check_movie_presense(movie_id):
    with connection: #bool of a list returned by a cursor.fetchall() from connection
        with connection.cursor() as cursor:
            return bool(cursor.execute("SELECT * FROM movies WHERE id=%s;", (movie_id,)).fetchall())

def check_user_presense(user_id):
    with connection:
        with connection.cursor() as cursor:
            return bool(cursor.execute("SELECT * FROM users WHERE username=%s;", (user_id,)).fetchall())

