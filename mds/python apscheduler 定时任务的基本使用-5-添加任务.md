python apscheduler 定时任务的基本使用-5-添加任务

# 1、添加定时任务

可以随时随地添加任务，不论调度器是否启动。如果未启动时，添加了定时任务，则会在调度器启动时，正常执行该任务。

添加方式有下面两种

## 1.1、通过add_job()函数添加

使用 add_job 方法添加任务，会返回一个Job对象，可以用于后续修改或删除任务，这是最普遍的添加任务的方式

例如

```python
def add_job():
    # 使用 add_job 方法添加任务 返回一个Job对象 可以用于后续修改或删除任务
    date = datetime.datetime.now() + datetime.timedelta(seconds=20)  # 可以添加datetime对象作为运行时间
    job = scheduler.add_job(my_job, trigger='date', args=['墨玉麒麟', 18], name="墨玉麒麟JOB", run_date=date,
                            timezone=shanghai)
    print(f'job:{job}')
    scheduler.print_jobs()
```

## 1.2、通过装饰器scheduled_job()添加

使用装饰器时，需要先实例化出一个调度器对象，然后调用调度器对象的scheduled_job方法

```python
@scheduler.scheduled_job('date', args=('装饰器参数',), run_date=run_date, name="装饰器", timezone=shanghai)
def my_job2(name):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log(f"这是由装饰器添加的任务, 名称是:{name}  现在时间:{now}")
```

说明：

- `scheduler`.scheduled_job中的`scheduler`是创建出的调度器对象

参考代码

```python
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

```



