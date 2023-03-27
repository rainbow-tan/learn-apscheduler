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
    log(f'我是{name} 现在时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    time.sleep(random.randint(1, 5))


def main():
    log(f'我是主线程, 现在时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    job_stores = {
        'default': SQLAlchemyJobStore(url='sqlite:///sqlite.sqlite3'),
    }
    executors = {
        "default": ThreadPoolExecutor(3),
    }
    shanghai = 'Asia/Shanghai'
    scheduler = BlockingScheduler(jobstores=job_stores, executors=executors)

    for i in range(5):
        scheduler.add_job(my_job, trigger='interval', args=[f'任务{i + 1}'],
                          name=f'任务{i + 1}', seconds=25, timezone=shanghai,
                          id=f'任务{i + 1}', replace_existing=True, misfire_grace_time=10)

    scheduler.start()
    # 使用了BlockingScheduler 则无法执行start后面的代码


"""
- 由于任务数总是多余于线程数，则先启动3个线程，执行三个任务，当三个任务执行完成后，空出了3个线程，此时看到还有两个任务需要执行（因为设置了misfire_grace_time=10，且任务时间总是少于10秒，所以任务不会Miss，）所以任务都能执行完成
- N个线程，M个任务数，M>N,misfire_grace_time=Q,每个任务执行时间总是小于Q,因此，不会出现Miss任务，除非M远远大于N，才会出现Miss任务
"""

if __name__ == '__main__':
    main()
