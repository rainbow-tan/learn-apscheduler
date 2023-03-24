import datetime
import random
import threading

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.blocking import BlockingScheduler


def log(msg):
    t = threading.currentThread()
    name = t.name
    ident = t.ident
    print(f"[{ident}][{name}]{msg}")  # 打印线程号和线程名称


def my_job(name):
    log(f'我是{name},现在时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} 随机数是:{random.randint(0, 100)}')


def main():
    log(f'我是主线程, 现在时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    shanghai = 'Asia/Shanghai'
    stores = {
        'default': SQLAlchemyJobStore(url='sqlite:///sqlite.sqlite3'),  # 默认使用这个数据库
        'sqlite2': SQLAlchemyJobStore(url='sqlite:///sqlite.sqlite3-2')  # 可以通过add_job时指定使用这个数据库
    }
    scheduler = BlockingScheduler(jobstores=stores)  # 执行线程最大10个 使用sqlite数据库

    run_date = datetime.datetime.now() + datetime.timedelta(seconds=20)  # 可以添加datetime对象作为运行时间
    scheduler.add_job(my_job, trigger='date', args=['数据库1'], name="数据库1JOB",
                      run_date=run_date, timezone=shanghai, id="数据库1ID")

    run_date = datetime.datetime.now() + datetime.timedelta(seconds=30)  # 可以添加datetime对象作为运行时间
    scheduler.add_job(my_job, trigger='date', args=['数据库2'], name="数据库2JOB",
                      run_date=run_date, timezone=shanghai, id="数据库2ID", jobstore='sqlite2')

    scheduler.print_jobs()

    scheduler.start()
    # 使用了BlockingScheduler 则无法执行start后面的代码


if __name__ == '__main__':
    main()
