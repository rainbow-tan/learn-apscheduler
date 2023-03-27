python apscheduler 定时任务的基本使用-8-线程执行器ThreadPoolExecutor

## 1、线程执行器ThreadPoolExecutor

先说个人总结

- 假设启动线程数为N，任务数为M，misfire_grace_time为F，则执行的逻辑是这样子的：
  - 先启动一个线程执行一个任务，如果还有任务，则再启动一个线程去执行，直到没有线程或者没有任务。
  - 当某个线程执行完成任务后，则会再去找是否还有任务，如果有，则判断超出任务执行的时间为多少秒，记为Q，如果Q大于F，则任务Miss，否则，继续执行该任务
  - 重复上一点，直到没有任务
  - 当下一轮任务到达时，如果上一轮任务还没结束，即没有空闲线程，则下一轮任务均skip。
  - 当下一轮任务到达时，如果上一轮任务有空闲线程，则顺序执行任务，任务还没结束的，直接skip，结束了的，直接就开始进行任务

- 每次最多起N个线程去执行任务，如果任务数M大于线程数，且不设置misfire_grace_time参数，则每次执行任务必Miss，且个位为M-N
- 执行的情况一般是一个线程一个任务，（除非任务很快结束，比如print一下就退出）当任务结束时，查看是否还有任务需要执行，有，就去执行，没有就结束。释放出线程。

- 判断是否还有任务需要执行，主要看misfire_grace_time参数，根据该参数判断是否任务还在合理的执行时间
- 当下一轮的触发器时间到了，如果上一轮任务还在执行，且没有空闲线程，则下一轮的任务均SKIP

- 出现Miss情况过多，则该考虑提高misfire_grace_time参数，或设置更大的线程池

例子

## （1）定义使用5个线程，任务数为4个

- 由于任务数总是少于线程数，肯定不会出现miss任务的情况

- 最多会启动5个线程来执行任务，如果任务执行过快，可能一个线程就执行完所有任务，如果任务执行过慢，则一个线程一个任务，执行完的线程又执行另一个任务

```python
import datetime
import random
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
    time.sleep(random.randint(1, 5))
    log(f'我是{name}')


def main():
    log(f'我是主线程, 现在时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    job_stores = {
        'default': SQLAlchemyJobStore(url='sqlite:///sqlite.sqlite3'),
    }
    executors = {
        "default": ThreadPoolExecutor(5),
    }
    shanghai = 'Asia/Shanghai'
    scheduler = BlockingScheduler(jobstores=job_stores, executors=executors)

    for i in range(4):
        scheduler.add_job(my_job, trigger='interval', args=[f'任务{i + 1}'],
                          name=f'任务{i + 1}', seconds=10, timezone=shanghai,
                          id=f'任务{i + 1}', replace_existing=True)

    scheduler.start()
    # 使用了BlockingScheduler 则无法执行start后面的代码


if __name__ == '__main__':
    main()

```

运行

![image-20230324163703930](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230324163703930.png)

## （2）定义使用5个线程，任务数为8个

- 由于任务数总是多余于线程数，且未设置misfire_grace_time参数，因此，每次都会有Miss任务

- 最多会启动5个线程来执行任务，一个线程一个任务，共8个任务，因此每次都有3个任务Miss

```python
import datetime
import random
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
    time.sleep(random.randint(1, 5))
    log(f'我是{name}')


def main():
    log(f'我是主线程, 现在时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    job_stores = {
        'default': SQLAlchemyJobStore(url='sqlite:///sqlite.sqlite3'),
    }
    executors = {
        "default": ThreadPoolExecutor(5),
    }
    shanghai = 'Asia/Shanghai'
    scheduler = BlockingScheduler(jobstores=job_stores, executors=executors)

    for i in range(8):
        scheduler.add_job(my_job, trigger='interval', args=[f'任务{i + 1}'],
                          name=f'任务{i + 1}', seconds=10, timezone=shanghai,
                          id=f'任务{i + 1}', replace_existing=True)

    scheduler.start()
    # 使用了BlockingScheduler 则无法执行start后面的代码


if __name__ == '__main__':
    main()
```

运行

![image-20230324164025022](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230324164025022.png)

## （3）定义使用3个线程，任务数为5个，设置misfire_grace_time=10

- 由于任务数总是多余于线程数，则先启动3个线程，执行三个任务，当三个任务执行完成后，空出了3个线程，此时看到还有两个任务需要执行（因为设置了misfire_grace_time=10，且任务时间总是少于10秒，所以任务不会Miss，）所以任务都能执行完成
- N个线程，M个任务数，M>N,misfire_grace_time=Q,每个任务执行时间总是小于Q,因此，不会出现Miss任务，除非M远远大于N，才会出现Miss任务

```python
import datetime
import random
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
    time.sleep(random.randint(1, 5))


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
                          name=f'任务{i + 1}', seconds=25, timezone=shanghai,
                          id=f'任务{i + 1}', replace_existing=True,misfire_grace_time=10)

    scheduler.start()
    # 使用了BlockingScheduler 则无法执行start后面的代码


"""

"""

if __name__ == '__main__':
    main()
```

## （4）定义使用3个线程，任务数为5个，设置misfire_grace_time=10,但10小于任务执行时间

- 首先启动3个线程执行任务，执行完三个任务后，空出的第一个线程去执行下一个任务，但发现此时已经超过任务执行时间12秒了，且12秒大于misfire_grace_time，因此，认为该任务错过了12秒。
- 此时第一个线程又接着看下一个任务，看到任务类似于上一个，错过了12秒，且不在misfire_grace_time范围内，因此认为任务Miss

```python
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
    time.sleep(12)


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
                          name=f'任务{i + 1}', seconds=20, timezone=shanghai,
                          id=f'任务{i + 1}', replace_existing=True, misfire_grace_time=10)

    scheduler.start()
    # 使用了BlockingScheduler 则无法执行start后面的代码


"""

"""

if __name__ == '__main__':
    main()
```

## （5）定义使用3个线程，任务数为5个，设置misfire_grace_time=1,但1小于任务执行时间,且任务时间大于下一轮时间

- 先启动3个线程跑3个任务，
- 任务还没跑完，到下一轮了，下一轮任务看到上一轮还在跑，且max_instances=1（默认最多同时存在一个任务在跑），认为上一次任务还没结束，还在跑，因此，直接跳过该次所有的任务，不管上一次任务真实跑了没，都直接SKIP掉了
- 对于上一轮任务，也有还没跑的，也直接跳过
- 上一轮任务跑完了，空出了线程，去看上一轮任务还有需要跑的，看到了，且超过了40秒，远大于misfire_grace_time，则任务Miss
- 以后每次都一样，skip一轮，且每次Miss两个任务

```python
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

"""

if __name__ == '__main__':
    main()
```

## （6）定义使用3个线程，任务数为4个，设置misfire_grace_time=10

- 开始3个线程去执行，线程1执行后，释放出来，继续执行任务4，且执行完后，也释放了线程1，因此线程1是空闲的
- 第二轮任务来了，线程1空闲，执行任务1，执行完，执行任务2，任务2还在上一轮，则skip跳过，执行任务3，任务上也还在上一轮执行，则跳过任务3，执行任务4
- 第三轮来了，现在都空闲，则类似上面两点，形成循环

```python
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
    if name=="任务1" or name=="任务4":
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
- 先启动3个线程跑3个任务，
- 任务还没跑完，到下一轮了，下一轮任务看到上一轮还在跑，且max_instances=1（默认最多同时存在一个任务在跑），认为上一次任务还没结束，还在跑，因此，直接跳过该次所有的任务，不管上一次任务真实跑了没，都直接SKIP掉了
- 对于上一轮任务，也有还没跑的，也直接跳过
- 上一轮任务跑完了，空出了线程，去看上一轮任务还有需要跑的，看到了，且超过了40秒，远大于misfire_grace_time，则任务Miss
- 以后每次都一样，skip一轮，且每次Miss两个任务
"""

if __name__ == '__main__':
    main()
```

运行

![image-20230327193424908](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230327193424908.png)