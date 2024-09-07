from flask import jsonify, request
from db import rc_db  # 假设这是处理 rc 表的数据库模块

def init_routes(app, handler):
    @app.route('/rc/add', methods=['POST'])
    def add_rc():
        data = request.get_json()
        rc_db.insert_rc(data.get("id"), data.get("name"), data.get("mcu"))
        return "1"

    @app.route('/rc/update', methods=['POST'])
    def update_rc():
        data = request.get_json()
        rc_db.update_rc(data.get("id"), data.get("name"), data.get("mcu"))
        return "1"

    @app.route('/rc/listAll')
    def list_all_rcs():
        list = rc_db.select_all_rcs()
        return jsonify(list)

    @app.route('/rc/delete')
    def delete_rc():
        id = request.args.get("id")
        rc_db.delete_rc(id)
        return "1"