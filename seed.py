"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Rating
from model import Movie
from model import MovieGenre
from model import Genre
from model import Job

from model import connect_to_db, db
from server import app
from datetime import datetime as dt


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()
    jobs = {}
    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        if jobs.get(occupation) is None:
            jobs[occupation] = len(jobs) + 1

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode,
                    job_id=jobs[occupation])
        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    for item in jobs.items():
        job = Job(job_id=item[1], title=item[0])
        db.session.add(job)

    # Once we're done, we should commit our work
    db.session.commit()


def load_genres():
    """Load genres to database"""
    print "Genres"

    Genre.query.delete()

    genre_names = ["unknown", "Action", "Adventure", "Animation",
                   "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                   "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi",
                   "Thriller", "War", "Western"]

    for name in genre_names:
        genre_name = Genre(name=name)
        db.session.add(genre_name)

    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""
    print "Movies"

    Movie.query.delete()

    with open("seed_data/u.item") as movies:
        for row in movies:
            row = row.rstrip()
            row = row.split("|")
            movie_id, title, released_at = row[:3]
            #index 3 is blank
            imdb_url = row[4]

            genres = row[5:]

            #convert date to datetime
            if released_at:
                released_at = dt.strptime(released_at, "%d-%b-%Y")
            else:
                released_at = None

            #strip movie year from title
            if title:
                title = title[:-7]
                title = title.decode("latin-1")
            else:
                title = None

            movie = Movie(movie_id=movie_id,
                          title=title,
                          released_at=released_at,
                          imdb_url=imdb_url)
            db.session.add(movie)

            #handle genres
            for i in range(len(genres)):
                if genres[i] == '1':
                    movie_genre = MovieGenre(movie_id=movie_id, genre_id=i+1)
                    db.session.add(movie_genre)

        db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""
    print "Ratings"

    Rating.query.delete()

    with open("seed_data/u.data") as ratings:
        for row in ratings:
            row = row.rstrip()
            row = row.split("\t")
            user_id, movie_id, score, timestamp = row

            rating = Rating(movie_id=movie_id,
                            user_id=user_id,
                            score=score)
            db.session.add(rating)

        db.session.commit()




def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_genres()
    load_movies()
    load_ratings()
    set_val_user_id()
