import pymysql

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

class PlayStatistics:
    def __init__(self, id, statc_type, statc_date, play_amount, total_money, time_amount):
        self.id = id
        self.statc_type = statc_type
        self.statc_date = statc_date
        self.play_amount = play_amount
        self.total_money = total_money
        self.time_amount = time_amount

# 插入一条记录
def insert_play_statistics(statistics):
    connection = connect_to_mysql()
    try:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO play_statistics (statc_type, statc_date, play_amount, total_money, time_amount)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (statistics['statc_type'], statistics['statc_date'], statistics['play_amount'], statistics['total_money'], statistics['time_amount']))
        connection.commit()
    finally:
        connection.close()

# 查询所有记录
def select_all_play_statistics():
    connection = connect_to_mysql()
    play_statistics = []
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM play_statistics"
            cursor.execute(sql)
            play_statistics = cursor.fetchall()
    finally:
        connection.close()
    return play_statistics

# 查询所有记录
def query_statistics(statc_type, start_time, end_time):
    connection = connect_to_mysql()
    play_statistics = []
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT * FROM play_statistics 
                where statc_date BETWEEN %s AND %s 
                and statc_type = %s
            """
            cursor.execute(sql)
            play_statistics = cursor.fetchall()
    finally:
        connection.close()
    return play_statistics

# 查询指定日期的统计数据 dateStr日期字符串，形如 yyyyMMdd,yyyyMM,yyyy
def select_statistics_for_date(dateStr):
    connection = connect_to_mysql()
    stats = None
    try:
        dateLen = len(dateStr)
        statc_type = '1'
        statc_date = dateStr
        if dateLen == 6:
            statc_type = '2'
        elif dateLen == 4:
            statc_type = '3'
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
            SELECT * FROM play_statistics 
            WHERE statc_type = %s AND statc_date = %s
            """
            cursor.execute(sql, (statc_type, statc_date))
            stats = cursor.fetchone()
    finally:
        connection.close()
    return stats


# 查询指 dateStr字符串，形如,yyyyMM,yyyy, 如果是yyyyMM。则查询指定月份的所有日统计说句。合并为月统计数据
# 如果是yyyyMM。则查询指定年份的所有月统计。合并为年统计
def select_for_month_or_year(dateStr):
    connection = connect_to_mysql()
    stats = []
    try:
        statc_date = f"{dateStr}%"
        dateLen = len(dateStr)
        statc_type = '1'
        if dateLen == 4:
            statc_type = '2'
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
            SELECT * FROM play_statistics 
            WHERE statc_type = %s AND statc_date like %s
            """
            cursor.execute(sql, (statc_type, statc_date))
            stats = cursor.fetchall()
    finally:
        connection.close()
    return stats


# 根据 ID 查询一条记录
def select_play_statistics_by_id(id):
    connection = connect_to_mysql()
    play_statistic = None
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM play_statistics WHERE id = %s"
            cursor.execute(sql, (id,))
            play_statistic = cursor.fetchone()
    finally:
        connection.close()
    return play_statistic

# 更新一条记录
def update_play_statistics(statistics):
    connection = connect_to_mysql()
    try:
        update_fields = {}
        if 'statc_type' in statistics and statistics['statc_type'] is not None:
            update_fields['statc_type'] = statistics['statc_type']
        if 'statc_date' in statistics and statistics['statc_date'] is not None:
            update_fields['statc_date'] = statistics['statc_date']
        if 'play_amount' in statistics and statistics['play_amount'] is not None:
            update_fields['play_amount'] = statistics['play_amount']
        if 'total_money' in statistics and statistics['total_money'] is not None:
            update_fields['total_money'] = statistics['total_money']
        if 'time_amount' in statistics and statistics['time_amount'] is not None:
            update_fields['time_amount'] = statistics['time_amount']

        if update_fields:
            keys = ', '.join(f"{key} = %s" for key in update_fields.keys())
            sql = f"UPDATE play_statistics SET {keys} WHERE id = %s"

            params = list(update_fields.values()) + [statistics['id']]
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
            connection.commit()
    finally:
        connection.close()

# 删除一条记录
def delete_play_statistics(id):
    connection = connect_to_mysql()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM play_statistics WHERE id = %s"
            cursor.execute(sql, (id,))
        connection.commit()
    finally:
        connection.close()