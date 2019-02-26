import threading
import time
import os
import psutil
flag = 0
lock = threading.Lock()
#运行多个fdtd计算线程，num1和num2表示的是开始和结束的fdtd计算线程的个数
#添加线程锁保证包含这几个线程的主线程运算结束之前其他的线程不会运算
def runsome(s,num1,num2,geneI):
    global flag
    lock.acquire()
    for i in range(int(num1),int(num2)):
         t = threading.Thread(target=runsing, args=(s,int(geneI),i,))
         t.start()
    #保证了xfdtd计算结束
    while(not judgeprocess("calcfdtd.exe")):
         time.sleep(1)
    lock.release()
#判断XFDTD是否计算完成的方法，因为要将其设为一个线程，而且必须在其他线程结束以后，所以加线程锁
def ifRunout():
    lock.acquire()
    global flag
    while (not judgeprocess("calcfdtd.exe")):
        time.sleep(1)
    flag = 1
    lock.release()
#运行单个XFDTD
def runsing(s,geneI,num):
    os.system("calcfdtd.exe -proc 4 {0}\\Step{1}\\{2}\\lktq".format(s,str(geneI),str(num)))
#判断系统中是否有某个进程在运行
#有俩个不安全的错误，一是如果这个进程在判断存在和使用这个线程之间消失的话，会抛出异常，
#                  一个解决方法是：尽量缩短判断和使用的时间，是这个事件法发生的概率尽可能的小，但是理论上肯定会发生。
#                另一个是：如果在程序之外自己开启了这个进程，程序无法判断这样会导致程序停止。
#                   解决方法：所以不能在程序运行期间自己开启XFDTD计算模型。
def judgeprocess(processname):
    pl = psutil.pids()
    for pid in pl:
        try:
             if not psutil.pid_exists(pid):
                continue
             elif  psutil.pid_exists(pid) and psutil.Process(pid).name() == processname:
                return False
        except psutil.NoSuchProcess:
            pass
        continue

    else:
        return True
#开启多个主线程计算模型，
#dir-模型的根目录
#begin- 开始的个体
#end-结束的个体
#step-步长
#geneI-遗传的代数
# 种群放置的目录应该这样设置：
# *(根目录就是第一个字符串参数dir)/2(一个数字代表迭代到第几代即geneI,这个例子是第二代)/1(代表的是第二代种群的第一个个体)
def runall(dir,begin,end,step,geneI):
    global flag
    flag = 0
    i=1
    while(begin+step*i<=end):
        t = threading.Thread(target=runsome, args=(dir, begin+step*(i-1), begin+step*i, geneI))
        t.start()
        i+=1
    t = threading.Thread(target=runsome, args=(dir, begin + step * (i - 1), end, geneI))
    t.start()
    # 判断这个计算程序是否运行结束，这个进程在最后一个计算进程开启之后开启，
    # 如果结束就把全局变量flag 设为1，以后的程序要判断这个flag，然后在运行
    t = threading.Thread(target=ifRunout())
    t.start()
    return flag
#runall('D:\CA\Simulation', 1, 51, 10, 1)



