python apscheduler 定时任务的基本使用-1-概念及组件构成

# 1、前言

我们需要执行定时任务，可以使用apscheduler这个框架，选择它的原因，是网上都说常用的就是这个。随大流嘛！[官方文档](https://apscheduler.readthedocs.io/en/3.x/userguide.html)

# 2、下载

```
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple apscheduler
```

# 3、组件构成

apscheduler由4种组件构成，分别是：

- 触发器（trigger）

  触发器中包含调度逻辑，每个作业都有自己的触发器来决定下次运行时间。除了它们自己初始配置以外，触发器完全是无状态的。

- 作业存储器（job store）

  存储被调度的作业，默认的作业存储器只是简单地把作业保存在内存中，其他的作业存储器则是将作业保存在数据库中，当作业被保存在一个持久化的作业存储器中的时候，该作业的数据会被序列化，并在加载时被反序列化，需要说明的是，**作业存储器不能共享调度器。**

  PS：不能两个调度器，共用一个数据库表，也就是只能存在一个调度器，两个调度器时，则应该使用两个数据库表

- 执行器（executor）

  处理作业的运行，通常通过在作业中提交指定的可调用对象到一个线程或者进程池来进行，当作业完成时，执行器会将通知调度器。

- 调度器（scheduler）

  配置作业存储器和执行器可以在调度器中完成。例如添加、修改、移除作业，根据不同的应用场景，可以选择不同的调度器

# 4、调度器的选择

您对调度器的选择主要取决于您的编程环境以及您将使用APScheduler的目的。可以使用以下调度器：

- BlockingScheduler：当调度程序是进程中唯一运行的程序时使用
- BackgroundScheduler：当您不使用下面的任何框架，并且希望调度器在应用程序的后台运行时使用
- AsyncIOScheduler：如果您的应用程序使用异步模块，则使用
- GeventScheduler：如果您的应用程序使用gevent，则使用
- TornadoSchedur：如果您正在构建Tornado应用程序，请使用
- TwistedScheduler：如果您正在构建Twisted应用程序，请使用
- QtScheduler：如果您正在构建Qt应用程序，请使用

# 5、执行器的选择

对执行器的选择取决于你使用上面哪些框架，大多数情况下，使用默认的ThreadPoolExecutor已经能够满足需求。如果你的应用涉及到CPU密集型操作，你可以考虑使用ProcessPoolExecutor来使用更多的CPU核心。你也可以同时使用两者，将ProcessPoolExecutor作为第二执行器。

但添加的任务，只能是一个执行器来执行，可以在添加任务时，指定执行器。

例如：你定义了两个执行器

```
executors = {
    "default": ThreadPoolExecutor(20),
    "processpool": ProcessPoolExecutor(5),
}
```

可以在添加任务时，指定选择哪一个执行器

```
scheduler.add_job(executor=executors['default'],***)
```

或者

```
scheduler.add_job(executor=executors['processpool'],***)
```

# 6、触发器的选择

添加定时任务时，需要为其选择触发器。触发器确定作业运行日期/时间的计算逻辑。APScheduler具有三种内置触发器类型：

date：当您想在某个时间点只运行一次作业时使用

interval：当您希望以固定的时间间隔运行作业时使用

cron：当您想在一天中的特定时间定期运行作业时使用

# 7、存储器的选择

存储器就是各种数据库，默认是存在内存中，一般就是测试使用，因为关闭程序，定时任务就失效了。常见的数据库是MongoDB、Sqlite、MySQL...

[github](https://github.com/rainbow-tan/learn-apscheduler)