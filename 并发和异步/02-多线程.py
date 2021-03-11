from queue import Queue
import threading
import random
import time

n = 0
glock = threading.Lock()
gcondition = threading.Condition()
gmoney = 1000
glocktimes = 10
gtimes = 0


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


def func3():
    global n
    glock.acquire() # 加锁
    for i in range(1000000):
        n+= 1
    glock.release() # 释放锁
    print('n:', n)


class Producer(threading.Thread):
    def run(self):
        global gmoney
        global gtimes
        while True:
            money = random.randint(100, 1000)
            glock.acquire()
            if gtimes >= glocktimes:
                glock.release()
                break
            gmoney += money
            print('%sproducer 生产了%d¥ 余额%d' % (threading.current_thread(), money, gmoney))
            gtimes += 1
            glock.release()
            time.sleep(0.5)



class Customer(threading.Thread):
    def run(self):
        global gmoney
        while True:
            money = random.randint(100, 1000)
            glock.acquire()
            if gmoney >= money:
                gmoney -= money
                print('%scustomer 消费了%d¥ 余额%d' % (threading.current_thread(), money, gmoney))
            else:
                print('%scustomer 预消费%d¥ 余额%d 不足！' % (threading.current_thread(), money, gmoney))
                if gtimes >= glocktimes:
                    glock.release()
                    break
            glock.release()
            time.sleep(0.5)



class Producer1(threading.Thread):
    def run(self):
        global gmoney
        global gtimes
        while True:
            money = random.randint(100, 1000)
            gcondition.acquire()
            if gtimes >= glocktimes:
                gcondition.release()
                break
            gmoney += money
            print('%sproducer 生产了%d¥ 余额%d' % (threading.current_thread(), money, gmoney))
            gtimes += 1
            # gcondition.notify # 
            gcondition.notify_all() # 通知所有在线等待的线程，notify和notify_all不回释放锁，所以要在release之前
            gcondition.release()
            time.sleep(0.5)



class Customer1(threading.Thread):
    def run(self):
        global gmoney
        while True:
            money = random.randint(100, 1000)
            gcondition.acquire()
            while gmoney < money:
                if gtimes >= glocktimes:
                    gcondition.release()
                    return # return会彻底结束整个函数
                print('%scustomer 预消费%d¥ 余额%d 不足！' % (threading.current_thread(), money, gmoney))
                gcondition.wait() # 将当前线程处于等待状态并会释放锁，能被其它线程用notify和notify_all唤醒，唤醒后继续等待上锁，上锁后继续执行下面的代码
            gmoney -= money
            print('%scustomer 消费了%d¥ 余额%d' % (threading.current_thread(), money, gmoney))
            gcondition.release()
            time.sleep(0.5)


def set_value(q):
    index = 0
    while True:
        q.put(index) # 将一个数据放到队列中，如果队列满了，阻塞等待
        index += 1
        # time.sleep(2)

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


    # for i in range(3):
    #     c = Customer1(name='customer%d' % i)
    #     c.start()

    # for i in range(5):
    #     p = Producer1(name='customer%d' % i)
    #     p.start()

    # for i in range(3):
    #     c = Customer(name='customer%d' % i)
    #     c.start()

    # for i in range(5):
    #     p = Producer(name='customer%d' % i)
    #     p.start()

    # for i in range(2):
    #     t = threading.Thread(target=func3)
    #     t.start()

    # print('执行主线程: %s' % threading.current_thread())
    # t1 = threading.Thread(target=func1)
    # t2 = threading.Thread(target=func2)
    # t3 = Func1()
    # t4 = Func2()
    # 
    # t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
    # # 查看有多少线程
    # print('查看所有线程:', threading.enumerate())


if __name__ == '__main__':
    main()

