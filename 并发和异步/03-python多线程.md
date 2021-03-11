> Python 多线程

线程运行在进程之中，一个进程被创建必定有一个主线程。

threading模块是python中专门用来实现多线程的

~~~python
import threading
import time


def func1():
    # 线程1
    for i in range(3):
        # 获取当前线程的名称
        print('执行func1: %s-%s' % (i, threading.current_thread()))
        time.sleep(1)


def func2():
    # 线程2
    for i in range(3):
        print('执行func2: %s-%s' % (i, threading.current_thread()))
        time.sleep(1)


class Func1(threading.Thread):
    def run(self):
        for i in range(3):
            # 获取当前线程的名称
            print('执行Func1: %s-%s' % (i, threading.current_thread()))
            time.sleep(1)


class Func2(threading.Thread):
    def run(self):
        for i in range(3):
            # 获取当前线程的名称
            print('执行Func2: %s-%s' % (i, threading.current_thread()))
            time.sleep(1)



def main():
    print('执行主线程: %s' % threading.current_thread())
    t1 = threading.Thread(target=func1)
    t2 = threading.Thread(target=func2)
    t3 = Func1()
    t4 = Func2()
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    # 查看有多少线程
    print('查看所有线程:', threading.enumerate())


if __name__ == '__main__':
    main()


~~~

~~~
执行主线程: <_MainThread(MainThread, started 4368891392)>
执行func1: 0-<Thread(Thread-1, started 123145489080320)>
执行func2: 0-<Thread(Thread-2, started 123145505869824)>
执行Func1: 0-<Func1(Thread-3, started 123145522659328)>
执行Func2: 0-<Func2(Thread-4, started 123145539448832)>
查看所有线程: [<_MainThread(MainThread, started 4368891392)>, <Thread(Thread-1, started 123145489080320)>, <Thread(Thread-2, started 123145505869824)>, <Func1(Thread-3, started 123145522659328)>, <Func2(Thread-4, started 123145539448832)>]
执行func2: 1-<Thread(Thread-2, started 123145505869824)>
执行func1: 1-<Thread(Thread-1, started 123145489080320)>
执行Func1: 1-<Func1(Thread-3, started 123145522659328)>
执行Func2: 1-<Func2(Thread-4, started 123145539448832)>
执行func2: 2-<Thread(Thread-2, started 123145505869824)>
执行func1: 2-<Thread(Thread-1, started 123145489080320)>
执行Func2: 2-<Func2(Thread-4, started 123145539448832)>
执行Func1: 2-<Func1(Thread-3, started 123145522659328)>
~~~

> 多线程共享全局变量

多线程都是在同一个进程中运行的，因此进程中的全局变量是多有线程共享的。由于线程的运行时无序的，有可能造成数据错乱。为了避免这一问题，我们需要在修改全局变量的时候加锁。

~~~python
import threading

n = 0
glock = threading.Lock()

def func3():
    global n
    glock.acquire() # 加锁
    for i in range(1000000):
        n+= 1
    glock.release() # 释放锁
    print('n:', n)


def main():
    for i in range(2):
        t = threading.Thread(target=func3)
        t.start()
~~~

~~~shell
n: 1000000
n: 2000000
~~~

> threading.Condition

上锁是一个很耗费CPU资源的行为，threading.Condition继承自threading.Lock，可以在没有数据的时候处于阻塞等待状态，一旦数据合适，可以使用notify相关的函数通知其他处于等待的线程，这样可以避免一些无用的上锁和解锁。

> Queue线程安全队列

在线程中，访问一些全局变量，加锁是一个经常的过程。如果想把数据存储在某些队列中，python中的queue模块提供了同步的、线程安全的队列类，包括先进先出FIFO、后入先出LIFO，这些队列都实现了锁原理（可以理解为原子操作，要么不做，要么都做完）能够在多线程中直接使用，可以使用队列来实现线程间的同步。

~~~python
def set_value(q):
    index = 0
    while True:
        q.put(index) # 将一个数据放到队列中，如果队列满了，阻塞等待
        index += 1
        time.sleep(2)

def get_value(q):
    while True:
        print(q.get()) # 从队列中去最后一个数据，也就是先进来的数据，如果队列为空，阻塞等待
        print(q.qsize()) # 返回队列的大小
        print(q.full()) # 判断队列是否满了
        print(q.empty()) # 判断队列是否为空




def main():
    q = Queue(4)
    t1 = threading.Thread(target=set_value, args=(q,))
    t2 = threading.Thread(target=get_value, args=(q,))

    t1.start()
    t2.start()
    
if __name__ == '__main__':
    main()
~~~

> GIL 全局解释器锁

python自带的解释器是CPython，CPython的多线程实际上是一个假的多线程（在多核CPU中只能利用一核，不能利用多核）同一时刻只有一个线程执行，为了保证同一时刻有多个线程执行，CPython中实现了一个全局解释器锁GIL，由于CPython解释器的能存管理不是线程安全的，所以GIL很有必要，它保证了同一时刻只有一个线程在执行。

GIL虽然是假的多线程，但是在处理I/O操作（比如文件读写和网络请求）上还是可以很大程度上提高效率。

因此：在高I/O操作上使用多线程，而在CPU计算（比如渲染3D模型）操作上使用多进程

