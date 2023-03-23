python apscheduler 定时任务的基本使用-3-interval触发器的使用

## 1、前言

interval触发器，按照一定的时间间隔运行任务。例如，每2秒运行一次任务，每分钟运行一次任务，每周运行一次任务，每5天运行一次任务。[官网interval](https://apscheduler.readthedocs.io/en/3.x/modules/triggers/interval.html#module-apscheduler.triggers.interval)

## 2、参数说明

参数如下，除了add_job的通用参数外，特有以下参数：

- weeks (int) – 隔多少周执行一次任务

- days (int) – 隔多少天执行一次任务

- hours (int) – 隔多少个小时执行一次任务

- minutes (int) – 隔几分钟执行一次任务

- seconds (int) – 隔几秒执行一次任务

- start_date - 指定开始时间 (datetime|str) – starting point for the interval calculation

  - 可以是datetime对象、date对象、"%Y-%m-%d %H:%M:%S"的字符串

- end_date - 指定结束时间

  - 可以是datetime对象、date对象、"%Y-%m-%d %H:%M:%S"的字符串

- timezone - 时区，中国就用'Asia/Shanghai'就行

- jitter 时间偏移量，单位秒

  - 在预定运行时间的基础上，加上一个随机的秒数

    例如 预定运行时间为10:20:20 偏移量为10 则真实运行时间期间为[10:20:20-10:20:30]

```python
import datetime
import threading

from apscheduler.schedulers.blocking import BlockingScheduler

"""
按照时间间隔执行任务
https://apscheduler.readthedocs.io/en/3.x/modules/triggers/interval.html#module-apscheduler.triggers.interval

参数
weeks (int) – number of weeks to wait
days (int) – number of days to wait
hours (int) – number of hours to wait
minutes (int) – number of minutes to wait
seconds (int) – number of seconds to wait
start_date (datetime|str) – starting point for the interval calculation
end_date (datetime|str) – latest possible date/time to trigger on
timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations
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


def seconds():
    # 每seconds秒运行一次任务
    scheduler.add_job(my_job, 'interval', args=['每两秒运行一次'], name="两秒一次任务", seconds=2)


def minutes():
    # 每minutes分钟运行一次任务
    scheduler.add_job(my_job, 'interval', args=['每1分钟运行一次'], name="一分钟一次任务", minutes=1)


def jitter():
    # 时间偏移量
    # 例如 预定运行时间为10:20:20 偏移量为10 则真实运行时间期间为[10:20:20-10:20:30]
    scheduler.add_job(my_job, 'interval', args=['每两秒运行一次'], name="两秒一次任务", seconds=2, jitter=3)


def minutes_and_seconds():
    # 混合使用参数
    scheduler.add_job(my_job, 'interval', args=['每1分钟两秒运行一次'], name="一分钟两秒一次任务", minutes=1, seconds=2)


def start_end():
    # 指定开始时间和结束时间 可只指定一个
    start_date = datetime.datetime.now() + datetime.timedelta(seconds=10)
    end_date = datetime.datetime.now() + datetime.timedelta(seconds=80)
    scheduler.add_job(my_job, 'interval', args=['开始结束时间'], name="开始结束时间",
                      seconds=2, start_date=start_date, end_date=end_date)


if __name__ == '__main__':
    log(f'我是主线程, 现在时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    shanghai = 'Asia/Shanghai'
    scheduler = BlockingScheduler()  # 默认存储在内存,执行线程最大10个
    scheduler.configure(timezone=shanghai)

    # seconds()
    # minutes()
    # jitter()
    # minutes_and_seconds()
    start_end()

    for one in scheduler.get_jobs():
        print(one, one.id)

    scheduler.start()
    # 使用了BlockingScheduler 则无法执行start后面的代码
```

[github](https://github.com/rainbow-tan/learn-apscheduler)