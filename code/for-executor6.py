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
    if name == "任务1" or name == "任务4":
        time.sleep(5)
    else:
        time.sleep(40)


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

    for i in range(4):
        scheduler.add_job(my_job, trigger='interval', args=[f'任务{i + 1}'],
                          name=f'任务{i + 1}', seconds=30, timezone=shanghai,
                          id=f'任务{i + 1}', replace_existing=True, misfire_grace_time=10)

    scheduler.start()
    # 使用了BlockingScheduler 则无法执行start后面的代码


"""
- 开始3个线程去执行，线程1执行后，释放出来，继续执行任务4，且执行完后，也释放了线程1，因此线程1是空闲的
- 第二轮任务来了，线程1空闲，执行任务1，执行完，执行任务2，任务2还在上一轮，则skip跳过，执行任务3，任务上也还在上一轮执行，则跳过任务3，执行任务4
- 第三轮来了，现在都空闲，则类似上面两点，形成循环
"""

if __name__ == '__main__':
    main()
