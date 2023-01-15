from datetime import datetime
import Utility.database as DBConnect
PROMPT = """\nWelcome to the movie watching app:
Add - Add new movie
Upcoming - View upcoming movies
All - View all movies
Mark - Mark watched movie
Watched - View watched movies
User - Add user to the app
Search - Search for a movie
Exit - Exit the app
Your choice: 
"""

def add_movie():
    title = input("Movie title: ").lower()
    if DBConnect.check_movie_presense(title):
        print("Movie already exists.")
    else:
        release_date = input("Release date as DD-MM-YYYY: ")
        release_date = datetime.strptime(release_date, "%d-%m-%Y")
        timestamp = release_date.timestamp()
        DBConnect.add_movie(title, timestamp)

def add_user():
    user = input("Select a user to input: ").lower()
    DBConnect.add_user(user)

def print_movies(movies, user, searched):
    if not user and not searched:
        movies = DBConnect.select_movies()
    if user:
        print(f"{user} has watched these movies: ")
    elif searched:
        print(f"{searched.title()} list results: ")
    for movie in movies:
        date = datetime.fromtimestamp(movie[2])
        date = date.strftime("%d-%m-%Y")
        print(f"{movie[0]}) {movie[1].title()}, released: {date}")

def print_watched_movies():
    user = input("User to search for: ").lower()
    if DBConnect.check_user_presense(user):
        watched_list = DBConnect.select_watched(user)
        print_movies(watched_list, user.title(), "")
    else:
        print("User not found.")

def print_upcoming_movies():
    date = datetime.now().timestamp()
    upcoming_list = DBConnect.select_upcoming(date)
    if upcoming_list:
        print_movies(upcoming_list, "", "Upcoming")
    else:
        print("No upcoming movies.")

def mark_movie():
    movie_id = int(input("Movie list id: "))
    user = input("Who watched the movie? (user): ").lower()
    if DBConnect.check_movie_presense(movie_id) and DBConnect.check_user_presense(user):
        DBConnect.mark_movie(user, movie_id)
    else:
        print("Movie or User does not exists.")

def delete_movie(): #Needs work
    title = input("Movie to delete: ").lower()
    if DBConnect.check_movie_presense(title):
        DBConnect.delete_movie(title)
    else:
        print("Movie is not in list.")

def search_movie():
    target = input("Movie to search for: ").lower()
    movie = DBConnect.search_movies(target)
    print_movies(movie, "", target)


def menu():
    DBConnect.create_table()
    while (choice := input(PROMPT)).lower() != 'exit':
        if choice == 'add':
            add_movie()
        elif choice == 'upcoming':
            print_upcoming_movies()
        elif choice == 'all':
            print_movies([0], "", "")
        elif choice == 'mark':
            mark_movie()
        elif choice == 'watched':
            print_watched_movies()
        elif choice == 'user':
            add_user()
        elif choice == 'search':
            search_movie()
        else:
            print("Invalid input.")

menu()