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
def insert_rc(id, name, mcu):
    connection = connect_to_mysql()
    try:
        with connection.cursor() as cursor:
            # 获取当前时间
            sql = "INSERT INTO rc (id, name, mcu) VALUES (%s, %s, %s)"
            cursor.execute(sql, (id, name, mcu))
        connection.commit()
    finally:
        connection.close()

# 查询所有记录
def select_all_rcs():
    connection = connect_to_mysql()
    rcs = []
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM rc order by id"
            cursor.execute(sql)
            rcs = cursor.fetchall()
    finally:
        connection.close()
    return rcs

# 根据 ID 查询一条记录
def select_rc_by_id(rc_id):
    connection = connect_to_mysql()
    rc = None
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM rc WHERE id = %s"
            cursor.execute(sql, (rc_id,))
            rc = cursor.fetchone()
    finally:
        connection.close()
    return rc

# 更新一条记录
def update_rc(rc_id, new_name, new_mcu):
    connection = connect_to_mysql()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE rc SET name = %s, mcu = %s WHERE id = %s"
            cursor.execute(sql, (new_name, new_mcu, rc_id))
        connection.commit()
    finally:
        connection.close()

# 删除一条记录
def delete_rc(rc_id):
    connection = connect_to_mysql()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM rc WHERE id = %s"
            cursor.execute(sql, (rc_id,))
        connection.commit()
    finally:
        connection.close()