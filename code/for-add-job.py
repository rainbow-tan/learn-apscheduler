import datetime
import threading

from apscheduler.schedulers.blocking import BlockingScheduler


def log(msg):
    t = threading.currentThread()
    name = t.name
    ident = t.ident
    print(f"[{ident}][{name}]{msg}")  # 打印线程号和线程名称


def my_job(name, age):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log(f"我是{name}, 今年{age}岁, 现在时间:{now}")
    scheduler.print_jobs()


def add_job():
    # 使用 add_job 方法添加任务 返回一个Job对象 可以用于后续修改或删除任务
    date = datetime.datetime.now() + datetime.timedelta(seconds=20)  # 可以添加datetime对象作为运行时间
    job = scheduler.add_job(my_job, trigger='date', args=['墨玉麒麟', 18], name="墨玉麒麟JOB", run_date=date,
                            timezone=shanghai)
    print(f'job:{job}')
    scheduler.print_jobs()


log(f'我是主线程, 现在时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
shanghai = 'Asia/Shanghai'
scheduler = BlockingScheduler()  # 默认存储在内存,执行线程最大10个

run_date = datetime.datetime.now() + datetime.timedelta(seconds=30)


@scheduler.scheduled_job('date', args=('装饰器参数',), run_date=run_date, name="装饰器", timezone=shanghai)
def my_job2(name):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log(f"这是由装饰器添加的任务, 名称是:{name}  现在时间:{now}")


add_job()

scheduler.print_jobs()

scheduler.start()
# 使用了BlockingScheduler 则无法执行start后面的代码
