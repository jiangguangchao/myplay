from flask import jsonify, request
from db import movies_db  # 假设这是处理 movies 表的数据库模块

def init_routes(app, handler):
    @app.route('/movies/add', methods=['POST'])
    def add_movie():
        data = request.get_json()
        movies_db.insert_movie(data.get("movie_id"), data.get("movie_name"))
        return "1"

    @app.route('/movies/update', methods=['POST'])
    def update_movie():
        data = request.get_json()
        movies_db.update_movie(data.get("movie_id"), data.get("movie_name"))
        return "1"

    @app.route('/movies/listAll')
    def list_all_movies():
        list = movies_db.select_all_movies()
        return jsonify(list)

    @app.route('/movies/delete')
    def delete_movie():
        movie_id = request.args.get("movie_id")
        movies_db.delete_movie(movie_id)
        return "1"