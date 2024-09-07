import pymysql
from datetime import datetime, timedelta

# MySQL 设置
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "jgc!#2022"
MYSQL_DB = "myplay"

# 连接到 MySQL 数据库
def connect_to_mysql():
    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
    return connection

# 插入一条记录
def insert_play(play_record):
    connection = connect_to_mysql()
    try:
        with connection.cursor() as cursor:
            # 使用 play_record 对象的属性
            sql = "INSERT INTO play_record (play_id, myplay, car_id, rc_id, start_Time, play_time, total_energy, used_energy, status,money) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (play_record.play_id, play_record.myplay, play_record.car_id, play_record.rc_id, play_record.start_time, play_record.play_time, play_record.total_energy, play_record.used_energy, play_record.status,play_record.money))
        connection.commit()
    finally:
        connection.close()

# 查询所有记录
def select_all_plays():
    connection = connect_to_mysql()
    play_records = []
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM play_record"
            cursor.execute(sql)
            play_records = cursor.fetchall()
    finally:
        connection.close()
    return play_records

def query_play(play_id, car_id, start_time, end_time):
    connection = connect_to_mysql()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 构建SQL查询语句
            sql = """
                SELECT * FROM play_record 
                WHERE start_Time BETWEEN %s AND %s
            """
            params = [start_time, end_time]

            # 如果car_id不是None，则添加到查询条件中
            if play_id:
                sql += " AND play_id = %s"
                params.append(play_id)

            if car_id:
                sql += " AND car_id = %s"
                params.append(car_id)

            cursor.execute(sql, tuple(params))
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

#查询某一天的数据
def select_records_for_date(date, status):
    connection = connect_to_mysql()
    records = []
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            start_of_day = datetime.combine(date, datetime.min.time())
            end_of_day = datetime.combine(date, datetime.max.time())
            sql = """
            SELECT * FROM play_record 
            WHERE start_Time >= %s AND start_Time <= %s and status = %s
            """
            cursor.execute(sql, (start_of_day, end_of_day, status))
            records = cursor.fetchall()
    finally:
        connection.close()
    return records


# 根据 ID 查询一条记录
def select_play_by_id(play_id):
    connection = connect_to_mysql()
    play_record = None
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM play_record WHERE play_id = %s"
            cursor.execute(sql, (play_id,))
            play_record = cursor.fetchone()
    finally:
        connection.close()
    return play_record


def update_play(play_record):
    connection = connect_to_mysql()  # 假设这个函数正确建立了数据库连接
    print(f"更新对象 {play_record}")
    try:
        # 初始化一个空字典来存储要更新的字段和值
        update_fields = {}

        # 检查每个字段，如果字段值不为空（这里假设空值包括None和空字符串''），则添加到更新字典中
        if play_record.myplay is not None:
            update_fields['myplay'] = play_record.myplay
        if play_record.car_id is not None:
            update_fields['car_id'] = play_record.car_id
        if play_record.rc_id is not None:
            update_fields['rc_id'] = play_record.rc_id
        if play_record.start_time is not None:
            update_fields['start_time'] = play_record.start_time
        if play_record.end_time is not None:
            update_fields['end_time'] = play_record.end_time
        if play_record.play_time is not None:
            update_fields['play_time'] = play_record.play_time
        if play_record.total_energy is not None:
            update_fields['total_energy'] = play_record.total_energy
        if play_record.used_energy is not None:
            update_fields['used_energy'] = play_record.used_energy
        if play_record.status is not None:
            update_fields['status'] = play_record.status
        if play_record.money is not None:
            update_fields['money'] = play_record.money

            # 如果至少有一个字段需要更新
        if update_fields:
            # 构建SQL语句
            # keys = ', '.join(update_fields.keys())
            # print(f"keys {keys}")
            # placeholders = ', '.join(['%s'] * len(update_fields))
            # print(f"placeholders {placeholders}")
            # sql = f"UPDATE play_record SET {keys} = ({placeholders}) WHERE play_id = %s"

            keys = ', '.join(f"{key} = %s" for key in update_fields.keys())
            sql = f"UPDATE play_record SET {keys} WHERE play_id = %s"

            print(f"执行sql {sql}")

            # 准备参数，包括更新值和play_id
            params = list(update_fields.values()) + [play_record.play_id]

            with connection.cursor() as cursor:
                cursor.execute(sql, params)
            connection.commit()
    finally:
        connection.close()



# 删除一条记录
def delete_play(play_id):
    connection = connect_to_mysql()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM play_record WHERE play_id = %s"
            cursor.execute(sql, (play_id,))
        connection.commit()
    finally:
        connection.close()