from database import Database
from data_objects.movie import Movie

def test_add_movie():
    db = Database("filmweb.db")
    db.clear()
    assert db.add_movie(Movie("zbyszek","tradalski","lorem lorem",10,"","")) == True
    assert db.add_movie(Movie("zbyszek","tradalski","lorem lorem",10,"","")) == False
    assert db.add_movie(Movie("","","lorem lorem",10,"","")) == False


def test_register_user():
    db = Database("filmweb.db")
    db.clear()
    assert db.register_user("","","") == None
    assert db.register_user("Bob","Smith","Smiths") != None
    assert db.register_user("Bob","Smith","Smith@net.com") == None
    assert db.register_user("Bob","Smith","Smith@net.com") == None

def test_add_review():
    db = Database("filmweb.db")
    db.clear()
    assert db.add_review(1,1,9) == False
    db.add_movie(Movie("zbyszek","tradalski","lorem lorem",10,"",""))
    db.register_user("Bob","Ross","ross@gmail.net")
    assert db.add_review(1,1,9) == True
    assert db.add_review(1,1,-10) == False

