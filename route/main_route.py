# main_route.py

from . import car_route, movies_route, movie_clips_route, rc_route

def init_routes(app, handler):
    car_route.init_routes(app, handler)
    rc_route.init_routes(app, handler)
    movies_route.init_routes(app, handler)
    movie_clips_route.init_routes(app, handler)

