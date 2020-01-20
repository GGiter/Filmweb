from data_objects.review import Review


def test_user_id():
    review1 = Review("", "", "")
    review2 = Review(10, "", "")
    review3 = Review(10.0, "", "")
    assert review1.get_user_id() == 0
    assert review2.get_user_id() == 10
    assert review3.get_user_id() == 0


def test_movie_id():
    review1 = Review("", "", "")
    review2 = Review("", 10, "")
    assert review1.get_movie_id() == 0
    assert review2.get_movie_id() == 10


def test_score_id():
    review1 = Review("", "", "")
    review2 = Review("", "", 10)
    assert review1.get_score() == 0
    assert review2.get_score() == 10
