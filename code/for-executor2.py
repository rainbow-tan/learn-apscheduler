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

    for i in range(8):
        scheduler.add_job(my_job, trigger='interval', args=[f'任务{i + 1}'],
                          name=f'任务{i + 1}', seconds=10, timezone=shanghai,
                          id=f'任务{i + 1}', replace_existing=True)

    scheduler.start()
    # 使用了BlockingScheduler 则无法执行start后面的代码


"""
- 由于任务数总是多余于线程数，且未设置misfire_grace_time参数，因此，每次都会有Miss任务

- 最多会启动5个线程来执行任务，一个线程一个任务，共8个任务，因此每次都有3个任务Miss
"""

if __name__ == '__main__':
    main()
