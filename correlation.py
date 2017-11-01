"""Pearson correlation."""

from math import sqrt
# from server import app


def pearson(pairs):
    """Return Pearson correlation for pairs.
    Using a set of pairwise ratings, produces a Pearson similarity rating.
    """

    series_1 = [float(pair[0]) for pair in pairs]
    series_2 = [float(pair[1]) for pair in pairs]

    sum_1 = sum(series_1)
    sum_2 = sum(series_2)

    squares_1 = sum([n * n for n in series_1])
    squares_2 = sum([n * n for n in series_2])

    product_sum = sum([n * m for n, m in pairs])

    size = len(pairs)

    numerator = product_sum - ((sum_1 * sum_2) / size)

    denominator = sqrt(
        (squares_1 - (sum_1 * sum_1) / size) *
        (squares_2 - (sum_2 * sum_2) / size)
    )

    if denominator == 0:
        return 0

    return numerator / denominator


#def judgement(user_id, title):
# def judgement(user_id, title):
#     m = Movie.query.filter_by(title=title).one()
#     u = User.query.get(user_id)
#     other_ratings = Rating.query.filter(Rating.movie_id == m.movie_id).all()
#     other_users = [r.user for r in other_ratings]
#     o = other_users[0]

#     u_ratings = {}
#     #for each rating in the user's ratings, add to dictionary the movie_id as
#     #a key, and rating as the value
#     for r in u.ratings:
#         u_ratings[r.movie_id] = r


#     paired_ratings = []
#     # go through other user's ratings
#     for o_rating in o.ratings:
#         # see if the user (u) rated the movie. If they did, create tuple;
#         # add to list
#         u_rating = u_ratings.get(o_rating.movie_id)
#         if u_rating is not None:
#             pair = (u_rating.score, o_rating.score)
#             paired_ratings.append(pair)
#     return paired_ratings


# if __name__ == "__main__":
#     connect_to_db(app)
    # pairs = judgement(945, "Beauty and the Beast")
    # corr = pearson(pairs)
    # print corr