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
def insert_movie(movie_id, movie_name):
    connection = connect_to_mysql()
    try:
        with connection.cursor() as cursor:
            # 获取当前时间
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = "INSERT INTO movies (movie_id, movie_name, create_time) VALUES (%s, %s, %s)"
            cursor.execute(sql, (movie_id, movie_name, current_time))
        connection.commit()
    finally:
        connection.close()

# 查询所有记录
def select_all_movies():
    connection = connect_to_mysql()
    movies = []
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM movies ORDER BY create_time"
            cursor.execute(sql)
            movies = cursor.fetchall()
    finally:
        connection.close()
    return movies

# 根据 ID 查询一条记录
def select_movie_by_id(movie_id):
    connection = connect_to_mysql()
    movie = None
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM movies WHERE movie_id = %s"
            cursor.execute(sql, (movie_id,))
            movie = cursor.fetchone()
    finally:
        connection.close()
    return movie

# 更新一条记录，只更新非空字段
def update_movie(movie_id, new_movie_name=None):
    connection = connect_to_mysql()
    updates = []
    values = []

    # 构建更新语句
    if new_movie_name is not None:
        updates.append("movie_name = %s")
        values.append(new_movie_name)

    # 如果有更新项，则执行更新
    if updates:
        values.append(movie_id)
        sql = f"UPDATE movies SET {', '.join(updates)} WHERE movie_id = %s"
        print(sql)
        print(f"Values: {values}")

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, tuple(values))
            connection.commit()
        finally:
            connection.close()

# 删除一条记录
def delete_movie(movie_id):
    connection = connect_to_mysql()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM movies WHERE movie_id = %s"
            cursor.execute(sql, (movie_id,))
        connection.commit()
    finally:
        connection.close()