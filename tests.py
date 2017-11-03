import unittest

from server import app
from model import db, connect_to_db
from fixtures import example_data


class RatingTests(unittest.TestCase):
    """Tests for my rating site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("View all movies", result.data)
        self.assertIn("View all users", result.data)

    def test_users(self):
        result = self.client.get("/users")
        self.assertIn("Users", result.data)

    def test_movies(self):
        result = self.client.get("/movies")
        self.assertIn("Filter by genre", result.data)

    def test_not_loggedin(self):
        result = self.client.get("/movies/2")
        self.assertNotIn("(amazing)", result.data)
        self.assertIn("We predict you'll give it: None", result.data)

    def test_new_user(self):
        result = self.client.post("/register",
                                  data={"email": "j@gmail.com",
                                        "password": "pass"},
                                  follow_redirects=True)
        self.assertIn("Movie Ratings", result.data)
        self.assertIn("added as a new user", result.data)

    def test_loggedin(self):
        result = self.client.post("/register",
                                  data={"email": "g@gmail.com",
                                        "password": "sday"},
                                  follow_redirects=True)
        self.assertIn("Movie Ratings", result.data)
        self.assertIn("logged in", result.data)

if __name__ == "__main__":
    unittest.main()
