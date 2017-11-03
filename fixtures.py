from model import User, Rating, Movie, Genre, MovieGenre, db


def example_data():

    u1 = User(email="f@gmail.com", password="sdaf")
    u2 = User(email="g@gmail.com", password="sday")
    u3 = User(email="h@gmail.com", password="sdafe")

    m1 = Movie(title="Toy Story")
    m2 = Movie(title="Top Gun")
    m3 = Movie(title="Up")

    r1 = Rating(movie_id=1, user_id=1, score=5)
    r2 = Rating(movie_id=2, user_id=1, score=4)
    r3 = Rating(movie_id=3, user_id=1, score=3)
    r4 = Rating(movie_id=1, user_id=2, score=4)
    r5 = Rating(movie_id=2, user_id=2, score=3)
    r6 = Rating(movie_id=3, user_id=2, score=2)
    r7 = Rating(movie_id=1, user_id=3, score=5)
    r8 = Rating(movie_id=2, user_id=3, score=4)

    g1 = Genre(name='Animation')
    g2 = Genre(name='Action')
    g3 = Genre(name="Children's")

    mg1 = MovieGenre(movie_id=1, genre_id=1)
    mg2 = MovieGenre(movie_id=1, genre_id=3)
    mg3 = MovieGenre(movie_id=3, genre_id=1)
    mg4 = MovieGenre(movie_id=3, genre_id=3)
    mg5 = MovieGenre(movie_id=2, genre_id=2)

    db.session.add_all([u1, u2, u3, m1, m2, m3, g1, g2, g3])
    db.session.commit()
    db.session.add_all([r1, r2, r3, r4, r5, r6, r7, r8, mg1, mg2, mg3, mg4, mg5])
    db.session.commit()
