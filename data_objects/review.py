
class Review():
    def __init__(self,user_id,movie_id,score,id = None):
        self.user_id = user_id if isinstance(user_id,int) else 0
        self.movie_id = movie_id if isinstance(movie_id,int) else 0
        self.score = score if isinstance(score,int) else 0

    def get_user_id(self):
        return self.user_id

    def get_movie_id(self):
        return self.movie_id
    
    def get_score(self):
        return self.score