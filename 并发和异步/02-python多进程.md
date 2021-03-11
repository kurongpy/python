> python多进程

在python中，使用 multiprocessing 模块的Process类创建子进程，这种方式支持跨平台。

~~~~python
from multiprocessing import Process
from time import sleep

def run_demo(name, age, **kwargs):
    print('子进程执行中，参数 name：%s, age：%d' % (name, age))
    print('kwargs:', kwar
    sleep(0.5)


if __name__=='__main__':
    # 创建子进程 target接收子进程执行的任务
    p = Process(target=run_demo, args=('kurong', 18), kwargs={'abc': 123})
    # 调用子进程
    p.start()
    print('执行主进程')

~~~~

Prpcess.join方法：阻塞主进程，使当前主进程等待调用join的子进程执行结束

~~~python
if __name__=='__main__':
    # 创建子进程 target接收子进程执行的任务
    p = Process(target=run_demo, args=('kurong', 18), kwargs={'abc': 123})
    # 调用子进程
    p.start()
    # join方法作用：阻塞主进程，使当前主进程等待调用join的子进程执行结束
    p.join()
    print('执行主进程')
~~~

进程池：专门用来装载进程的容器。

multiprocessing 模块的Pool类的`__init__`可以传递一个参数，用来指定进程池中同一时刻最多能拥有多少个进程，父进程不会等待进程池中的子进程执行完毕才退出，而是父进程中的代码执行完毕后立即退出。

子进程的资源来源于父进程，子进程创建运行时会完完全全复制一份父进程的资源，如果子进程过多，会很消耗性能和资源，进程池能够很好的解决这一点。

~~~python
 if __name__=='__main__':  
  	pool = Pool(3) # 同一时刻只能有3个子进程运行

    for i in range(10):
      	# 向进程池内添加进程，并且并行执行
        pool.apply_async(run_demo, args=('kurong', 18), kwds={'abc': 123})
    
    pool.close() # 关闭进程池，不能够再添加进程
    pool.join() # 阻塞主进程，等待所有子进程结束

    print('执行主进程')
~~~

父子进程数据共享问题：

创建一个子进程，子进程会拷贝父进程所有资源作为运行环境，子进程中的变量可能跟父进程一样，但其实是存储在另外的内存区域，因此父进程与子进程之间的数据是不共享的。

~~~python
from multiprocessing import Process

age = 22

def demo():
    global age
    age += 1
    print('子进程age:',age)


if __name__=='__main__':
    p = Process(target=demo)
    p.start()
    print('主进程age:', age)
    print('执行主进程')
~~~

~~~bash
# 执行结果：    
主进程age: 22
执行主进程
子进程age: 23
~~~

Queue消息队列：

进程之间的数据是不共享的，因此两个进程之间想要使用相同的数据，就需要进程间的通信。进程间的通信有多种方式，常用的有管道（pipe）和队列（queue）

```python
from multiprocessing import Process, Queue


def write(q):
    for i in [1, 2, 3]:
        q.put(i)
    print('写入消息完毕')


def read(q):
    while True:
        try:
            # block参数默认为True，如果q中消息为空get读取消息则会阻塞，block参数为False，如果q中消息为空则抛出异常
            msg = q.get(block=False)
            print('读取到消息：',msg)
        except:
            print('读取消息完毕')
            break


if __name__=='__main__':
    q = Queue()
    pw = Process(target=write, args=(q, ))
    pr = Process(target=read, args=(q, ))

    pw.start()
    pr.start()

    pw.join()
    # print(q.qsize()) # 获取消息队列中消息的数量
    print(q.full()) # 判断消息队列是否满了
    print(q.empty()) # 判断消息队列是否空了
    print('执行主进程')
```

```bash
# 输出结果
写入消息完毕
读取到消息： 1
读取到消息： 2
读取到消息： 3
读取消息完毕
False
True
执行主进程
```

Pool进程间通信

Pool和Queue不能够共用，因此Pool进程间通信使用multiprocessing 模块的Manager类，在Manager类下有一个Queue对象能实现Pool进程间通行。

```python
if __name__=='__main__':
    q = Manager().Queue()
    pool = Pool(2)
    # apply方法：向进程池添加进程，并且并发执行
    pool.apply(write,args=(q,))
    pool.apply(read, args=(q,))
    pool.close()
    pool.join()

    print('执行主进程')
```

```bash
写入消息完毕
读取到消息： 1
读取到消息： 2
读取到消息： 3
读取消息完毕
执行主进程
```

