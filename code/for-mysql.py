import datetime
import random
import threading

from apscheduler.executors.pool import ThreadPoolExecutor
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
    mysql_name = "gip"
    mysql_host = "xxx.xx.xxx.xx"
    mysql_port = 3306
    mysql_user = "root"
    mysql_password = "88888888"
    # 通过pymysql这个库来操作数据库
    url = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_name}?charset=utf8"
    job_stores = {
        "default": SQLAlchemyJobStore(
            url=url,
            tablename="aps-task",  # 表名
            engine_options={"pool_pre_ping": True, "pool_recycle": 25200},
        ),  # 默认使用这个数据库
        'sqlite': SQLAlchemyJobStore(url='sqlite:///sqlite.sqlite3'),  # 另一个为sqlite的存储器
    }

    executors = {
        "default": ThreadPoolExecutor(20),
    }

    job_defaults = {
        "coalesce": True,
        "max_instances": 1,
    }

    scheduler = BlockingScheduler(jobstores=job_stores, job_defaults=job_defaults, executors=executors)

    run_date = datetime.datetime.now() + datetime.timedelta(seconds=20)  # 可以添加datetime对象作为运行时间
    scheduler.add_job(my_job, trigger='date', args=['数据库1'], name="数据库1JOB",
                      run_date=run_date, timezone=shanghai, id="数据库1ID")

    run_date = datetime.datetime.now() + datetime.timedelta(seconds=30)  # 可以添加datetime对象作为运行时间
    scheduler.add_job(my_job, trigger='date', args=['数据库2'], name="数据库2JOB",
                      run_date=run_date, timezone=shanghai, id="数据库2ID", jobstore='sqlite')
    scheduler.print_jobs()

    scheduler.start()
    # 使用了BlockingScheduler 则无法执行start后面的代码


if __name__ == '__main__':
    main()
