from data_objects.review import Review


def test_user_id():
    review = Review("", "", "")
    assert review.get_user_id() == 0


def test_movie_id():
    review = Review("", "", "")
    assert review.get_movie_id() == 0


def test_score_id():
    review = Review("", "", "")
    assert review.get_score() == 0
