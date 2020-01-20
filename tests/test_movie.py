from data_objects.movie import Movie


def test_title():
    movie = Movie(0, "", "", "", "", "")
    assert movie.get_title() == ""


def test_director():
    movie = Movie("", 0, "", "", "", "")
    assert movie.get_title() == ""


def test_description():
    movie = Movie("", "", 0, "", "", "")
    assert movie.get_title() == ""


def test_actors():
    movie = Movie("", "", "", "", 0, "")
    assert movie.get_title() == ""


def test_genre():
    movie = Movie("", "", "", "", "", 0)
    assert movie.get_title() == ""


def test_duration():
    movie = Movie("", "", "", "", "", "")
    assert movie.get_duration() == 0
