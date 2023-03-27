import datetime
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
    time.sleep(12)


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
                          name=f'任务{i + 1}', seconds=20, timezone=shanghai,
                          id=f'任务{i + 1}', replace_existing=True, misfire_grace_time=10)

    scheduler.start()
    # 使用了BlockingScheduler 则无法执行start后面的代码


"""
- 首先启动3个线程执行任务，执行完三个任务后，空出的第一个线程去执行下一个任务，但发现此时已经超过任务执行时间12秒了，且12秒大于misfire_grace_time，因此，认为该任务错过了12秒。
- 此时第一个线程又接着看下一个任务，看到任务类似于上一个，错过了12秒，且不在misfire_grace_time范围内，因此认为任务Miss

"""

if __name__ == '__main__':
    main()
