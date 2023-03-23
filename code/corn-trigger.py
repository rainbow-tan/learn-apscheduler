import datetime
import threading

from apscheduler.schedulers.blocking import BlockingScheduler

"""
类似Unix的cron执行任务 匹配cron表达式时执行任务
https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html#module-apscheduler.triggers.cron

参数
year (int|str) – 4-digit year
month (int|str) – month (1-12)
day (int|str) – day of month (1-31)
week (int|str) – ISO week (1-53)
day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
hour (int|str) – hour (0-23)
minute (int|str) – minute (0-59)
second (int|str) – second (0-59)
start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)
jitter (int|None) – delay the job execution by jitter seconds at most
"""


def log(msg):
    t = threading.currentThread()
    name = t.name
    ident = t.ident
    print(f"[{ident}][{name}]{msg}")  # 打印线程号和线程名称


def my_job(msg):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log(f"现在时间:{now}, 消息:{msg}")
    for job in scheduler.get_jobs():
        print(job, job.id)


def second():
    # 每两秒
    scheduler.add_job(my_job, 'cron', args=('每两秒',), second='*/2')


def second_5():
    # 每分钟的5秒
    scheduler.add_job(my_job, 'cron', args=('每分钟的5秒',), second='5')


def second_3_5():
    # 每分钟的3,5秒
    scheduler.add_job(my_job, 'cron', args=('每分钟的3,5秒',), second='3,5')


def start_end():
    start_date = datetime.datetime.now() + datetime.timedelta(seconds=10)
    end_date = datetime.datetime.now() + datetime.timedelta(seconds=80)
    scheduler.add_job(my_job, 'cron', args=('start_end',), second='*/2', start_date=start_date, end_date=end_date)


if __name__ == '__main__':
    log(f'我是主线程, 现在时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    shanghai = 'Asia/Shanghai'
    scheduler = BlockingScheduler()  # 默认存储在内存,执行线程最大10个
    scheduler.configure(timezone=shanghai)

    # second()
    # second_3_5()
    start_end()

    for one in scheduler.get_jobs():
        print(one, one.id)

    scheduler.start()
    # 使用了BlockingScheduler 则无法执行start后面的代码
