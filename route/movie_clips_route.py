from flask import jsonify, request
from db import movie_clips_db  # 假设这是处理 movie_clips 表的数据库模块

def init_routes(app, handler):
    @app.route('/movieClips/add', methods=['POST'])
    def add_movie_clip():
        data = request.get_json()
        movie_clips_db.insert_movie_clip(data.get("clip_id"), data.get("movie_id"), data.get("clip_name"))
        return "1"

    @app.route('/movieClips/update', methods=['POST'])
    def update_movie_clip():
        data = request.get_json()
        movie_clips_db.update_movie_clip(data.get("clip_id"), data.get("movie_id"), data.get("clip_name"))
        return "1"

    @app.route('/movieClips/listAll')
    def list_all_movie_clips():
        list = movie_clips_db.select_all_movie_clips()
        return jsonify(list)

    @app.route('/movieClips/delete')
    def delete_movie_clip():
        clip_id = request.args.get("clip_id")
        movie_clips_db.delete_movie_clip(clip_id)
        return "1"