class Review():
    """
    class that represents data about review from database
    """
    def __init__(self, user_id, movie_id, score):
        self._user_id = user_id if isinstance(user_id, int) else 0
        self._movie_id = movie_id if isinstance(movie_id, int) else 0
        self._score = score if isinstance(score, int) else 0

    def get_user_id(self):
        return self._user_id

    def get_movie_id(self):
        return self._movie_id

    def get_score(self):
        return self._score
