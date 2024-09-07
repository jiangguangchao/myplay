import pymysql
import datetime

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
def insert_car(id, name, mcu):
    connection = connect_to_mysql()
    try:
        with connection.cursor() as cursor:
            # 获取当前时间
            sql = "INSERT INTO car (id, name, mcu) VALUES (%s, %s, %s)"
            cursor.execute(sql, (id, name, mcu))
        connection.commit()
    finally:
        connection.close()

# 查询所有记录
def select_all_cars():
    connection = connect_to_mysql()
    cars = []
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM car ORDER BY id"
            cursor.execute(sql)
            cars = cursor.fetchall()
    finally:
        connection.close()
    return cars

# 根据 ID 查询一条记录
def select_car_by_id(car_id):
    connection = connect_to_mysql()
    car = None
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM car WHERE id = %s"
            cursor.execute(sql, (car_id,))
            car = cursor.fetchone()
    finally:
        connection.close()
    return car


# 更新一条记录，只更新非空字段
def update_car(car_id, new_name=None, new_mcu=None):
    connection = connect_to_mysql()
    updates = []
    values = []

    # 构建更新语句
    if new_name is not None:
        updates.append("name = %s")
        values.append(new_name)
    if new_mcu is not None:
        updates.append("mcu = %s")
        values.append(new_mcu)

    # 如果有更新项，则执行更新
    if updates:
        values.append(car_id)
        sql = f"UPDATE car SET {', '.join(updates)} WHERE id = %s"
        print(sql)
        print(f"Values: {values}")

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, tuple(values))
            connection.commit()
        finally:
            connection.close()

# 删除一条记录
def delete_car(car_id):
    connection = connect_to_mysql()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM car WHERE id = %s"
            cursor.execute(sql, (car_id,))
        connection.commit()
    finally:
        connection.close()