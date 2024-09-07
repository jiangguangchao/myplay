import pymysql
# import list

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
def insert_car_play(car_play):
    connection = connect_to_mysql()
    try:
        with connection.cursor() as cursor:
            # 使用 car_play 对象的属性
            sql = "INSERT INTO car_play (play_id, myplay, car_id, rc_id, start_Time, play_time, total_energy, used_energy, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (car_play.play_id, car_play.myplay, car_play.car_id, car_play.rc_id, car_play.start_time, car_play.play_time, car_play.total_energy, car_play.used_energy, car_play.status))
        connection.commit()
    finally:
        connection.close()

# 查询所有记录
def select_all_car_plays():
    connection = connect_to_mysql()
    car_plays = []
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM car_play"
            cursor.execute(sql)
            car_plays = cursor.fetchall()
    finally:
        connection.close()
    return car_plays

# 根据 ID 查询一条记录
def select_car_play_by_id(play_id):
    connection = connect_to_mysql()
    car_play = None
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM car_play WHERE play_id = %s"
            cursor.execute(sql, (play_id,))
            car_play = cursor.fetchone()
    finally:
        connection.close()
    return car_play

# 更新一条记录
def update_car_play(car_play):
    connection = connect_to_mysql()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE car_play SET myplay = %s, car_id = %s, rc_id = %s, start_Time = %s, play_time = %s, total_energy = %s, used_energy = %s WHERE play_id = %s"
            cursor.execute(sql, (car_play.myplay, car_play.car_id, car_play.rc_id, car_play.start_time, car_play.play_time, car_play.total_energy, car_play.used_energy, car_play.play_id))
        connection.commit()
    finally:
        connection.close()

def update_car_play2(car_play):
    connection = connect_to_mysql()  # 假设这个函数正确建立了数据库连接
    print(f"更新对象 {car_play}")
    try:
        # 初始化一个空字典来存储要更新的字段和值
        update_fields = {}

        # 检查每个字段，如果字段值不为空（这里假设空值包括None和空字符串''），则添加到更新字典中
        if car_play.myplay is not None:
            update_fields['myplay'] = car_play.myplay
        if car_play.car_id is not None:
            update_fields['car_id'] = car_play.car_id
        if car_play.rc_id is not None:
            update_fields['rc_id'] = car_play.rc_id
        if car_play.start_time is not None:
            update_fields['start_time'] = car_play.start_time
        if car_play.end_time is not None:
            update_fields['end_time'] = car_play.end_time
        if car_play.play_time is not None:
            update_fields['play_time'] = car_play.play_time
        if car_play.total_energy is not None:
            update_fields['total_energy'] = car_play.total_energy
        if car_play.used_energy is not None:
            update_fields['used_energy'] = car_play.used_energy
        if car_play.status is not None:
            update_fields['status'] = car_play.status

            # 如果至少有一个字段需要更新
        if update_fields:
            # 构建SQL语句
            # keys = ', '.join(update_fields.keys())
            # print(f"keys {keys}")
            # placeholders = ', '.join(['%s'] * len(update_fields))
            # print(f"placeholders {placeholders}")
            # sql = f"UPDATE car_play SET {keys} = ({placeholders}) WHERE play_id = %s"

            keys = ', '.join(f"{key} = %s" for key in update_fields.keys())
            sql = f"UPDATE car_play SET {keys} WHERE play_id = %s"

            print(f"执行sql {sql}")

            # 准备参数，包括更新值和play_id
            params = list(update_fields.values()) + [car_play.play_id]

            with connection.cursor() as cursor:
                cursor.execute(sql, params)
            connection.commit()
    finally:
        connection.close()



# 删除一条记录
def delete_car_play(play_id):
    connection = connect_to_mysql()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM car_play WHERE play_id = %s"
            cursor.execute(sql, (play_id,))
        connection.commit()
    finally:
        connection.close()