from data.database import Database
from data_objects.movie import Movie


def test_add_movie():
    db = Database("filmweb.db")
    db.clear()
    assert db.add_movie(Movie("zbyszek", "tradalski", "lorem lorem",
                        10, "", "")) is True
    assert db.add_movie(Movie("zbyszek", "tradalski", "lorem lorem",
                        10, "", "")) is False
    assert db.add_movie(Movie("", "", "lorem lorem", 10, "", "")) is False


def test_get_movie_reviews():
    db = Database("filmweb.db")
    db.clear()
    db.add_movie(Movie("zbyszek", "tradalski", "lorem lorem", 10, "", ""))
    db.register_user("Bob", "Smith", "Smith@net.com")
    db.add_review(1, 1, 2)
    assert len(db.get_movie_reviews(Movie("", "", "lorem lorem",
                                    10, "", "", None, 0))) == 0
    assert len(db.get_movie_reviews(Movie("zbyszek", "tradalski",
                                    "lorem lorem", 10, "", "", None, 1))) == 1


def test_register_user():
    db = Database("filmweb.db")
    db.clear()
    assert db.register_user("", "", "") is None
    # invalid email
    assert db.register_user("Bob", "Smith", "Smiths") is None
    assert db.register_user("Bob", "Smith", "Smith@net.com") is not None
    # duplicate user
    assert db.register_user("Bob", "Smith", "Smith@net.com") is None


def test_get_field():
    db = Database("filmweb.db")
    db.clear()
    db.register_user("Bob", "Smiths", "Smith@net.com")
    assert db.get_field_by_id("users", "login", 1) == "Bob"
    # invalid field name
    assert db.get_field_by_id("users", "logins", 1) is None
    # invalid data table name
    assert db.get_field_by_id("users", "loginss", 1) is None
    assert db.get_field_by_parameter("users", "login", "id", 1) == "Bob"
    assert db.get_field_by_parameter(
        "users", "email", "login", "Bob") == "Smith@net.com"


def test_add_review():
    db = Database("filmweb.db")
    db.clear()
    # no such user and movie
    assert db.add_review(1, 1, 9) is False
    db.add_movie(Movie("zbyszek", "tradalski", "lorem lorem", 10, "", ""))
    db.register_user("Bob", "Ross", "ross@gmail.net")
    assert db.add_review(1, 1, 9) is True
    # invalid score
    assert db.add_review(1, 1, -10) is False

