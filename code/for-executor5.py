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

    for i in range(5):
        scheduler.add_job(my_job, trigger='interval', args=[f'任务{i + 1}'],
                          name=f'任务{i + 1}', seconds=30, timezone=shanghai,
                          id=f'任务{i + 1}', replace_existing=True, misfire_grace_time=2)

    scheduler.start()
    # 使用了BlockingScheduler 则无法执行start后面的代码


"""
- 先启动3个线程跑3个任务，
- 任务还没跑完，到下一轮了，下一轮任务看到上一轮还在跑，且max_instances=1（默认最多同时存在一个任务在跑），认为上一次任务还没结束，还在跑，因此，直接跳过该次所有的任务，不管上一次任务真实跑了没，都直接SKIP掉了
- 对于上一轮任务，也有还没跑的，也直接跳过
- 上一轮任务跑完了，空出了线程，去看上一轮任务还有需要跑的，看到了，且超过了40秒，远大于misfire_grace_time，则任务Miss
- 以后每次都一样，skip一轮，且每次Miss两个任务
"""

if __name__ == '__main__':
    main()
