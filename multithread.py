import threading
from multiprocessing import Pool, Manager
import os
from time import sleep
import time
from tkinter import *


def test_thread(q):
    task_bank = []
    for i in range(4):
        task_bank.append(threading.Thread(target=test_do, args=(i, q)))
    for task in task_bank:
        task.start()
    for task in task_bank:
        task.join()


def test_do(num, q):
    str1 = '{} {} start\n'.format(os.getpid(), num)
    print(str1, end='')
    while q.empty():
        pass
    str = '{} {} end\n'.format(os.getpid(), num)
    while not q.empty():
        pass
    print(str, end='')


class GuiTest:

    def __init__(self, n):
        self.root = Tk()
        self.root.geometry('460x240')
        self.root.title('test')
        lb = Label(text=str(n))
        lb.pack()
        self.root.mainloop()

def con(q):
    str1 = '{} con start\n'.format(os.getpid())
    print(str1, end='')
    sleep(3)
    q.put('1')
    str = '{} con end\n'.format(os.getpid())
    print(str, end='')
    sleep(1)
    q.get()


if __name__ == '__main__':
    # root = Tk()
    # root.geometry('460x240')
    # root.title('test')
    # b1 = Button(root, text='1', command=GuiTest)
    # b1.pack()
    # root.mainloop()
    p = Pool(3)
    q = Manager().Queue(1)
    t1 = time.time()
    print(q.empty())
    for i in range(2):
        p.apply_async(GuiTest, args=(i, ))
        # p.apply_async(test_thread, args=(q, ))
    # p.apply_async(con, args=(q, ))
    p.close()
    p.join()
    # t2 = time.time()
    # print(t2-t1)