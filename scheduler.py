import time
import datetime


from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger

from financialdata.producer import Update


def sent_crawler_task():
    logger.info("sent_crawler_task")
    today = (
        datetime.datetime.today().date().strftime("%Y%m%d")
    )
    print('run time {}'.format(today))
    Update("taiwan_stock_price", today, today)

def run_initial_task_if_needed():
    now = datetime.datetime.now()
    target_time = now.replace(hour=15, minute=0, second=0, microsecond=0)
    logger.info(f"Current time: {now}, Target time: {target_time}")
    sent_crawler_task()
    if now > target_time:  # If the current time is after 15:00
        sent_crawler_task()
        logger.info("Running initial task as current time is after 15:00.")


def main():
    scheduler = BackgroundScheduler(timezone='Asia/Taipei')
    scheduler.add_job(
        id="sent_crawler_task",
        func=sent_crawler_task, 
        trigger="cron",
        hour="15",
        minute="0",
        day_of_week="mon-fri",
        # args=["taiwan_stock_price"]
    )
    logger.info("sent_crawler_task")
    scheduler.start()
    run_initial_task_if_needed()
    logger.info("bbbbbbbbbbbbbbb")
    print('aaa')
    

if __name__ == "__main__":
    main()
    while True:
        time.sleep(600)
