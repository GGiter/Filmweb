
class Review():
    def __init__(self,user_id,movie_id,score,id = None):
        self.user_id = user_id
        self.movie_id = movie_id
        self.score = score

    def get_user_id(self):
        return self.user_id

    def get_movie_id(self):
        return self.movie_id
    
    def get_score(self):
        return self.score