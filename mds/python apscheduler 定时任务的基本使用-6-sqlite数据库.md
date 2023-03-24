python apscheduler 定时任务的基本使用-6-sqlite数据库

# 1、使用sqlite数据库步骤

1. 定义数据库字典

   ![image-20230324153334730](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230324153334730.png)

2. 指定调度器的存储器

   ![image-20230324153346314](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230324153346314.png)

3. 添加任务即可

   ![image-20230324153400249](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230324153400249.png)

直接上代码

```python
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

    scheduler.print_jobs()

    scheduler.start()
    # 使用了BlockingScheduler 则无法执行start后面的代码


if __name__ == '__main__':
    main()
```

运行后数据库

![image-20230324152406049](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230324152406049.png)

## 2、添加任务指定不同存储器

通过公共参数jobstore指定即可

![image-20230324153144226](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230324153144226.png)

运行后保存到不同的数据库

![image-20230324153042303](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230324153042303.png)

代码

```python
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
```

[github](https://github.com/rainbow-tan/learn-apscheduler)