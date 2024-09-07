import pymysql
from datetime import datetime, timedelta
from db import play_record_db, play_statistics_db
from dateutil.relativedelta import relativedelta



def today_statistics():
    process_daily_statistics(datetime.now().date())

def current_month():
    process_month_or_year_statistics(datetime.now().date().strftime('%Y%m'))

def current_year():
    process_month_or_year_statistics(datetime.now().date().strftime('%Y'))

def yesterday_statistics():
    process_daily_statistics(datetime.now().date()- relativedelta(days=1))

def last_month():
    last_month = datetime.now().date()- relativedelta(months=1)
    process_month_or_year_statistics(last_month.strftime('%Y%m'))

def last_year():
    last_year = datetime.now().date()- relativedelta(years=1)
    process_month_or_year_statistics(last_year.strftime('%Y'))

# 统计记录
def aggregate_records(records):
    daily_stats = {
        'play_amount': 0,
        'total_money': 0.00,
        'time_amount': 0,
    }

    for record in records:
        daily_stats['play_amount'] += 1
        daily_stats['total_money'] += float(record.get('money', 0.00))
        daily_stats['time_amount'] += record.get('play_time', 0)

    return daily_stats


# 统计记录
def aggregate_statistics(statistics):
    stats = {
        'play_amount': 0,
        'total_money': 0.00,
        'time_amount': 0,
    }

    for sta in statistics:
        stats['play_amount'] += sta.get('play_amount', 0)
        stats['total_money'] += float(sta.get('total_money', 0.00))
        stats['time_amount'] += sta.get('time_amount', 0)

    return stats


# 主函数
def process_daily_statistics(target_date):

    target_date_str = target_date.strftime('%Y%m%d')
    existing_stats = play_statistics_db.select_statistics_for_date(target_date_str)
    if existing_stats and target_date != datetime.now().date():
        print("指定日期不是今天且指定日期统计数据已经存在，不再统计")
        return


    print(f"目标日期 {target_date_str}")
    # 查询指定日期的记录
    records = play_record_db.select_records_for_date(target_date, "10")#状态是已结束的
    # 统计记录
    daily_stats = aggregate_records(records)



    if existing_stats:
        print(f"已经存在日统计:{target_date_str}，开始更新")
        #更新
        daily_stats['id'] = existing_stats['id']
        play_statistics_db.update_play_statistics(daily_stats)
    else:
        print(f"不存在日统计:{target_date_str}，开始新增")
        daily_stats['statc_type'] = '1'
        daily_stats['statc_date'] = target_date_str
        play_statistics_db.insert_play_statistics(daily_stats)

    print(f"日统计{target_date_str}数据已存入play_statistics表。")

def process_month_or_year_statistics(target_date_str):
    date_desc = "月"
    statc_type = "2"
    if len(target_date_str) == 4:
        date_desc = "年"
        statc_type = "3"

    existing_stats = play_statistics_db.select_statistics_for_date(target_date_str)
    if existing_stats and target_date_str != datetime.now().date().strftime('%Y%m'):
        print(f"指定{date_desc}:{target_date_str}不是本{date_desc}且统计数据已经存在，不再统计")
        return

    # 查询指定日期的记录
    statistics = play_statistics_db.select_for_month_or_year(target_date_str)
    # 合并
    stats = aggregate_statistics(statistics)

    if existing_stats:
        #更新
        print(f"已经存在{date_desc}统计:{target_date_str}，开始更新")
        stats['id'] = existing_stats['id']
        stats['statc_date'] = existing_stats['statc_date']
        play_statistics_db.update_play_statistics(stats)
    else:
        #新增
        print(f"不存在{date_desc}统计:{target_date_str}，开始新增")
        stats['statc_type'] = statc_type
        stats['statc_date'] = target_date_str
        play_statistics_db.insert_play_statistics(stats)

    print(f"{date_desc}统计:{target_date_str}数据已存入play_statistics表。")




