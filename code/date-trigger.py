import datetime
import threading

from apscheduler.schedulers.blocking import BlockingScheduler

"""
date 触发器
https://apscheduler.readthedocs.io/en/3.x/modules/triggers/date.html#module-apscheduler.triggers.date

参数
run_date (datetime|str) – the date/time to run the job at
timezone (datetime.tzinfo|str) – time zone for run_date if it doesn’t have one already

说明
在指定的时间点, 只会运行一次任务
"""


def log(msg):
    t = threading.currentThread()
    name = t.name
    ident = t.ident
    print(f"[{ident}][{name}]{msg}")  # 打印线程号和线程名称


def my_job(name, age):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log(f"我是{name}, 今年{age}岁, 现在时间:{now}")
    for job in scheduler.get_jobs():
        print(job, job.id)


if __name__ == '__main__':
    log(f'我是主线程, 现在时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    shanghai = 'Asia/Shanghai'
    scheduler = BlockingScheduler()  # 默认存储在内存,执行线程最大10个

    run_date = datetime.datetime.now() + datetime.timedelta(seconds=20)  # 可以添加datetime对象作为运行时间
    scheduler.add_job(my_job, trigger='date', args=['墨玉麒麟', 18], name="墨玉麒麟JOB", run_date=run_date, timezone=shanghai)

    run_date = datetime.date(2023, 3, 24)  # 可以添加date对象作为运行时间
    scheduler.add_job(my_job, trigger='date', args=['墨子', 18], name="墨子JOB", run_date=run_date, timezone=shanghai)

    run_date = (datetime.datetime.now() + datetime.timedelta(seconds=30)).strftime("%Y-%m-%d %H:%M:%S")  # 可以添加字符串作为运行时间
    scheduler.add_job(my_job, trigger='date', args=['青鳞', 18], name="青鳞JOB", run_date=run_date, timezone=shanghai)

    scheduler.add_job(my_job, trigger='date', args=['现在时', 18], name="现在时", timezone=shanghai)  # 不指定运行时间, 则直接运行

    run_date = datetime.datetime.now() - datetime.timedelta(hours=10)  # 可以添加datetime对象作为运行时间 添加过去的时间, 则直接报Miss
    scheduler.add_job(my_job, trigger='date', args=['过去时', 18], name="过去时", run_date=run_date,
                      timezone=shanghai)  # 不指定运行时间, 则直接运行

    for one in scheduler.get_jobs():
        print(one, one.id)

    scheduler.start()
    # 使用了BlockingScheduler 则无法执行start后面的代码
