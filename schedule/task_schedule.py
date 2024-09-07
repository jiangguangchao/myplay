from apscheduler.schedulers.background import BackgroundScheduler
from service import play_statistics_service
from datetime import datetime, timedelta

# 统计今天
def current_statistics():
    play_statistics_service.today_statistics()
    play_statistics_service.current_month()
    play_statistics_service.current_year()

def history_statistics():
    play_statistics_service.yesterday_statistics()
    play_statistics_service.last_month()


# 初始化 APScheduler
def init_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=current_statistics, trigger="interval", seconds=60)
    scheduler.start()
    app.apscheduler = scheduler