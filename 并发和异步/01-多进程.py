from multiprocessing import Process, Pool, Queue, Manager
from time import sleep
import os

age = 22

def run_demo(name, age, **kwargs):
    print('子进程执行中，参数 name：%s, age：%d' % (name, age))
    print('kwargs:', kwargs)
    print('子进程id：', os.getpid())
    print('父进程id：', os.getppid())
    sleep(0.5)


# 使用类的方式创建子进程
class MyProcess(Process):
    # 使用类的方式创建子进程必须要重写run方法
    def run(self):
        print('子进程id：', os.getpid())

def demo():
    global age
    age += 1
    print('子进程age:',age)


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
    # p = Process(target=demo)
    # p.start()
    # 创建子进程 target接收子进程执行的任务
    # p = Process(target=run_demo, args=('kurong', 18), kwargs={'abc': 123})
    # mp = MyProcess()

    # 调用子进程
    # p.start()
    # mp.start()

    # join方法作用：阻塞主进程，使当前主进程等待调用join的子进程执行结束
    # p.join()
    # p.join(2) # 设置阻塞时间，超过阻塞时间，不管子进程有没有执行完毕，都要执行主进程
    # mp.join(2)

    # pool = Pool(3) # 同一时刻只能有3个子进程运行

    # for i in range(10):
    #     # 向进程池内添加进程，并且并行执行
    #     pool.apply_async(run_demo, args=('kurong', 18), kwds={'abc': 123})
    
    # pool.close() # 关闭进程池，不能够再添加进程
    # pool.join() # 阻塞主进程，等待所有子进程结束
    # print('主进程age:', age)
    # q = Queue()
    # pw = Process(target=write, args=(q, ))
    # pr = Process(target=read, args=(q, ))

    # pw.start()
    # pr.start()

    # pw.join()
    # # print(q.qsize()) # 获取消息队列中消息的数量
    # print(q.full()) # 判断消息队列是否满了
    # print(q.empty()) # 判断消息队列是否空了
    q = Manager().Queue()
    pool = Pool(2)
    # apply方法：向进程池添加进程，并且并发执行
    pool.apply(write,args=(q,))
    pool.apply(read, args=(q,))
    pool.close()
    pool.join()

    print('执行主进程')
    