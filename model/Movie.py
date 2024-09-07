
class Movie:
    def __init__(self, movie_id=None, movie_name=""):
        self.movie_id = movie_id  
        self.movie_name = movie_name  

    def __str__(self):  
        return f"Movie ID: {self.movie_id}, Name: {self.movie_name}"
  
