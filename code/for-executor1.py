import datetime
import random
import threading
import time

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.blocking import BlockingScheduler


def log(msg):
    t = threading.currentThread()
    name = t.name
    ident = t.ident
    print(f"[{ident}][{name}]{msg}")  # 打印线程号和线程名称


def my_job(name):
    time.sleep(random.randint(1, 5))
    log(f'我是{name}')


def main():
    log(f'我是主线程, 现在时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    job_stores = {
        'default': SQLAlchemyJobStore(url='sqlite:///sqlite.sqlite3'),
    }
    executors = {
        "default": ThreadPoolExecutor(5),
    }
    shanghai = 'Asia/Shanghai'
    scheduler = BlockingScheduler(jobstores=job_stores, executors=executors)

    for i in range(4):
        scheduler.add_job(my_job, trigger='interval', args=[f'任务{i + 1}'],
                          name=f'任务{i + 1}', seconds=10, timezone=shanghai,
                          id=f'任务{i + 1}', replace_existing=True)

    scheduler.start()
    # 使用了BlockingScheduler 则无法执行start后面的代码


"""
- 由于任务数总是少于线程数，肯定不会出现miss任务的情况

- 最多会启动5个线程来执行任务，如果任务执行过快，可能一个线程就执行完所有任务，如果任务执行过慢，则一个线程一个任务，执行完的线程又执行另一个任务
"""

if __name__ == '__main__':
    main()
