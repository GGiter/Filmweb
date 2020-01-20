from data_objects.movie import Movie


def test_title():
    movie1 = Movie(0, "", "", "", "", "")
    movie2 = Movie("title", "", "", "", "", "")
    assert movie1.get_title() == ""
    assert movie2.get_title() == "title"


def test_director():
    movie1 = Movie("", 0, "", "", "", "")
    movie2 = Movie("", "director", "", "", "", "")
    assert movie1.get_director() == ""
    assert movie2.get_director() == "director"


def test_description():
    movie1 = Movie("", "", 0, "", "", "")
    movie2 = Movie("", "", "description", "", "", "")
    assert movie1.get_description() == ""
    assert movie2.get_description() == "description"


def test_actors():
    movie1 = Movie("", "", "", "", 0, "")
    movie2 = Movie("", "", "", "", "actors", "")
    assert movie1.get_actors() == ""
    assert movie2.get_actors() == "actors"


def test_genre():
    movie1 = Movie("", "", "", "", "", 0)
    movie2 = Movie("", "", "", "", "", "genre")
    assert movie1.get_genre() == ""
    assert movie2.get_genre() == "genre"


def test_duration():
    movie1 = Movie("", "", "", "", "", "")
    movie2 = Movie("", "", "", 10, "", "")
    assert movie1.get_duration() == 0
    assert movie2.get_duration() == 10
