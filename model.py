"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
import correlation

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.job_id'))

    def similarity(self, other):
        """Return Pearson rating for user compared to other user."""

        u_ratings = {}
        paired_ratings = []

        for r in self.ratings:
            u_ratings[r.movie_id] = r

        for r in other.ratings:
            u_r = u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append((u_r.score, r.score))

        if paired_ratings:
            return correlation.pearson(paired_ratings)

        else:
            return 0.0

    def predict_rating(self, movie):
        """Predict user's rating of a movie."""

        other_ratings = movie.ratings

        similarities = [
            (self.similarity(r.user), r)
            for r in other_ratings
        ]

        similarities.sort(reverse=True)

        similarities = [(sim, r) for sim, r in similarities
                        if sim > 0]

        if not similarities:
            return None

        numerator = sum([r.score * sim for sim, r in similarities])
        denominator = sum([sim for sim, r in similarities])

        return numerator/denominator

    def __repr__(self):
        """Provide better representation."""
        return "<User user_id={} email={}>".format(self.user_id, self.email)


class Job(db.Model):
    """Job table for users"""

    __tablename__ = "jobs"

    job_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)

    users = db.relationship("User", backref=db.backref("job"))


class Movie(db.Model):
    """Movie details."""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    released_at = db.Column(db.DateTime)
    imdb_url = db.Column(db.String(200))

    def __repr__(self):
        """Provide better representation."""
        return "<Movie movie_id={} title={}>".format(self.movie_id, self.title)

    genres = db.relationship("Genre", secondary="moviegenres", backref="movies")


class Rating(db.Model):
    """List of ratings by user for movie."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    #Define relationship to user
    user = db.relationship("User", backref=db.backref("ratings",
                                                      order_by=rating_id))

    #Define relationship to movie
    movie = db.relationship("Movie", backref=db.backref("ratings",
                                                        order_by=rating_id))

    def __repr__(self):
        """Provide better representation."""
        return "<Rating rating_id={} movie_id={} user_id={} score={}>".format(
            self.rating_id, self.movie_id, self.user_id, self.score)


class Genre(db.Model):
    """Make table for genres."""

    __tablename__ = "genres"

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        """Provide better representation."""
        return "<Genre name={}>".format(self.name)


class MovieGenre(db.Model):
    """Association table for model and genre tables."""

    __tablename__ = "moviegenres"

    mg_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), nullable=False)

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
    db.create_all()
