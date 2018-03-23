#coding=utf-8
#测试

from multiprocessing import Process, Queue
import os, time, random

#写数据进程执行的代码:
def write(q):
    print('Process to write: %s parent pid is : %s' % (os.getppid(), os.getpid()))
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)  #写入队列
        time.sleep(random.random())

# 读数据进程执行的代码:
def read(q):
    print('Process22 to read: %s  parent pid is : %s ' % (os.getpid(), os.getppid()))
    for value in ['D', 'E', 'F']:
        print('Put %s to queue...' % value)
        q.put(value)  #写入队列
        time.sleep(random.random())

if __name__ == '__main__':
    # 父进程创建Queue实例，并传给各个子进程：
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    time1=time.time()
    pw.start()  # 启动子进程pw，写入:
    pr.start()   # 启动子进程pr，读取:
    print("共耗时:"+str(round((time.time()-time1),3))+"秒")
    pw.join()  # 等待pw结束:
    pr.join() # 等待pr结束:
    print("共耗时:"+str(round((time.time()-time1),3))+"秒")

    #pr.terminate()  # pr进程里是死循环，无法等待其结束，只能强行终止