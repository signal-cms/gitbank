import hashlib
import multiprocessing
import os
from time import sleep
import threading
from tkinter import *
from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.keys import Keys
from multiprocessing import Manager, Pool
import getpass


class MajorGiftGui:

    def __init__(self, q, pool_num):
        self.pool_num = pool_num
        self.driver = None
        self.signal = threading.Event()
        self.driver_bank = []
        self.cookies_bank = []
        self.driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver.exe')
        self.root = Tk()
        self.root.geometry('460x240')
        self.root.title('主程序名字长度不一样')
        self.is_ready = False
        self.qu = q
        self.driver_list = [[], [], [], [], ]
        lb1 = Label(self.root, text='填写信息，点击启动后开始自动刷取')
        lb1.place(relx=0.1, rely=0.01, relwidth=0.8, relheight=0.1)

        lb20 = Label(self.root, text='主播房间号')
        lb20.place(relx=0.01, rely=0.12, relwidth=0.2, relheight=0.1)
        self.room_id = Entry(self.root)
        self.room_id.place(relx=0.23, rely=0.12, relwidth=0.7, relheight=0.1)
        # lb21 = Label(self.root, text='多开数')
        # lb21.place(relx=0.53, rely=0.12, relwidth=0.15, relheight=0.1)
        # self.thread_num = Entry(self.root)
        # self.thread_num.place(relx=0.68, rely=0.12, relwidth=0.3, relheight=0.1)

        lb30 = Label(self.root, text='刷第几个礼物')
        lb30.place(relx=0.01, rely=0.23, relwidth=0.2, relheight=0.1)
        self.gift_order = Entry(self.root)
        self.gift_order.place(relx=0.23, rely=0.23, relwidth=0.7, relheight=0.1)
        # lb31 = Label(self.root, text='刷几次')
        # lb31.place(relx=0.53, rely=0.23, relwidth=0.15, relheight=0.1)
        # self.gift_time = Entry(self.root)
        # self.gift_time.place(relx=0.68, rely=0.23, relwidth=0.3, relheight=0.1)

        lb4 = Label(self.root, text='每次刷几个')
        lb4.place(relx=0.01, rely=0.34, relwidth=0.22, relheight=0.1)
        self.gift_num = Entry(self.root)
        self.gift_num.place(relx=0.23, rely=0.34, relwidth=0.7, relheight=0.1)
        lb5 = Button(self.root, text='浏览器开启数', command=self.set_driver_num)
        lb5.place(relx=0.01, rely=0.45, relwidth=0.22, relheight=0.1)
        self.driver_num = Entry(self.root)
        self.driver_num.place(relx=0.23, rely=0.45, relwidth=0.7, relheight=0.1)
        # lb6 = Label(self.root, text='刷手密码')
        # lb6.place(relx=0.01, rely=0.56, relwidth=0.2, relheight=0.1)
        # self.password = Entry(self.root)
        # self.password.place(relx=0.23, rely=0.56, relwidth=0.3, relheight=0.1)
        # btn9 = Button(self.root, text='一键退出', command=self.quit_driver)
        # btn9.place(relx=0.6, rely=0.2, relwidth=0.3, relheight=0.3)
        btn1 = Button(self.root, text='初始化', command=self.init_para)
        btn1.place(relx=0.0325, rely=0.67, relwidth=0.2, relheight=0.1)
        btn2 = Button(self.root, text='登录界面', command=self.login)
        btn2.place(relx=0.28, rely=0.67, relwidth=0.2, relheight=0.1)
        btn3 = Button(self.root, text='完成登录', command=self.get_cookie)
        btn3.place(relx=0.52, rely=0.67, relwidth=0.2, relheight=0.1)
        btn4 = Button(self.root, text='测试', command=self.gift_test)
        btn4.place(relx=0.78, rely=0.67, relwidth=0.2, relheight=0.1)
        btn5 = Button(self.root, text='复制窗口', command=self.anchor_room)
        btn5.place(relx=0.0325, rely=0.78, relwidth=0.2, relheight=0.1)
        btn6 = Button(self.root, text='准备', command=self.ready_go)
        btn6.place(relx=0.28, rely=0.78, relwidth=0.2, relheight=0.1)
        # btn7 = Button(self.root, text='开始/继续←', command=self.start_signal)
        # btn7.place(relx=0.52, rely=0.78, relwidth=0.2, relheight=0.1)
        btn8 = Button(self.root, text='退出一个浏览器', command=self.quit_one_driver)
        btn8.place(relx=0.78, rely=0.78, relwidth=0.2, relheight=0.1)
        # btn_convenience = Button(self.root, text='快捷键测试')
        # btn_convenience.bind_all('<KeyPress>', self.event_handler)
        # btn_convenience.place()
        lb7 = Label(self.root, text='提示')
        lb7.place(relx=0.02, rely=0.89, relwidth=0.1, relheight=0.1)
        self.tip = Entry(self.root)
        self.tip.place(relx=0.13, rely=0.89, relwidth=0.8, relheight=0.1)
        self.root.mainloop()

    # design for convenience command
    def event_handler(self, event):
        if event.keysym == 'Left':
            self.start_signal()
        if event.keysym == 'Right':
            self.stop_signal()

    # tips
    def set_tips(self, tip):
        if self.tip.get():
            self.tip.delete(0, END)
        self.tip.insert(END, tip)

    # driver num
    def set_driver_num(self):
        if self.driver_num.get():
            self.driver_num.delete(0, END)
        self.driver_num.insert(END, len(self.driver_bank))

    def init_para(self):
        self.driver_bank = []
        # if self.thread_num.get():
        #     self.thread_num.delete(0, END).delete(0, END)
        # self.thread_num.insert(END, '8')
        if self.gift_order.get():
            self.gift_order.delete(0, END)
        self.gift_order.insert(END, '2')
        if self.gift_num.get():
            self.gift_num.delete(0, END)
        self.gift_num.insert(END, '1')
        self.is_ready = False
        self.set_tips('初始化成功,默认刷第二个礼物（锤子）,默认每次刷一个')

    # get login page
    def login(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        # options.add_argument('blink-settings=imagesEnabled=false')
        self.driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=options)
        self.driver.implicitly_wait(3)
        # login page
        self.driver.get(
            'https://cnpassport.laifeng.com/mini_login.htm?lang=zh_cn&appName=youku&appEntrance=laifeng&styleType='
            'vertical&bizParams=&notLoadSsoView=true&notKeepLogin=false&isMobile=false&pid=20160918PLF000695&rnd='
            '0.7248185733783202')
        self.set_tips('打开首页成功，请登录！')

    def get_cookie(self):
        cookies = self.driver.get_cookies()
        self.cookies_bank = []
        for ck in cookies:
            self.cookies_bank.append({
                'domain': ck.get('domain'),
                'name': ck.get('name'),
                'path': ck.get('path'),
                'value': ck.get('value')
            })
        if self.qu.empty():
            for i in range(self.pool_num - 1):
                self.qu.put([self.cookies_bank, self.room_id.get(), self.gift_order.get(), self.gift_num.get()])
        self.set_tips('获取登录信息成功,请测试')

    def gift_test(self):
        if not self.cookies_bank:
            self.set_tips('请按完成登录,获取登录信息后再进行测试')
            return None
        if self.room_id.get():
            self.driver.get('https://v.laifeng.com/{}'.format(self.room_id.get()))
            sleep(1)
            while self.select_gift(self.driver):
                try:
                    self.driver.find_element_by_xpath(
                        '//*[@id="LF-chat-gift"]/div/div/div/div[1]/div[1]/div/div/div/ul/li[{}]'.format(
                            self.gift_order.get())
                    ).click()
                except Exception:
                    pass
            # delete key:
            for i in range(5):
                try:
                    self.driver.find_element_by_xpath(
                        '//*[@id="LF-chat-gift"]/div/div/div/div[2]/div[3]/div[2]/div/input'
                    ).send_keys(Keys.BACK_SPACE)
                except Exception:
                    pass
            # input gift num
            try:
                self.driver.find_element_by_xpath(
                    '//*[@id="LF-chat-gift"]/div/div/div/div[2]/div[3]/div[2]/div/input'
                ).send_keys(self.gift_num.get())
            except Exception:
                pass
            if not self.driver_bank:
                self.driver_bank.append(self.driver)
        else:
            self.set_tips('请输入房间号')
        self.set_driver_num()

    @staticmethod
    def set_gift_num(driver):
        content = driver.page_source
        html = etree.HTML(content)
        num_content = html.xpath(
            '//*[@id="LF-chat-gift"]/div/div/div/div[2]/div[3]/div[2]/div/input/@value'
        )[0]
        return not num_content == ''

    def anchor_room(self):
        if self.is_ready:
            self.set_tips('已经入准备状态,无法复制窗口')
            return None
        if self.room_id.get():
            self.copy_driver()
        else:
            self.set_tips('请输入房间号')

    def copy_driver(self):
        if not self.cookies_bank:
            self.set_tips('请按完成登录,获取登录信息后再进行复制窗口')
            return None
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('blink-settings=imagesEnabled=false')
        driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=options)
        driver.get(
            'https://cnpassport.laifeng.com/mini_login.htm?lang=zh_cn&appName=youku&appEntrance=laifeng&styleType='
            'vertical&bizParams=&notLoadSsoView=true&notKeepLogin=false&isMobile=false&pid=20160918PLF000695&rnd='
            '0.7248185733783202')
        for cookie in self.cookies_bank:
            driver.add_cookie(cookie)
        driver.get('https://v.laifeng.com/{}'.format(self.room_id.get()))
        sleep(1)
        while self.select_gift(driver):
            try:
                driver.find_element_by_xpath(
                    '//*[@id="LF-chat-gift"]/div/div/div/div[1]/div[1]/div/div/div/ul/li[{}]'.format(
                        self.gift_order.get())
                ).click()
            except Exception:
                pass
        # delete key:
        for i in range(5):
            try:
                self.driver.find_element_by_xpath(
                    '//*[@id="LF-chat-gift"]/div/div/div/div[2]/div[3]/div[2]/div/input'
                ).send_keys(Keys.BACK_SPACE)
            except Exception:
                pass
        # input gift num
        try:
            self.driver.find_element_by_xpath(
                '//*[@id="LF-chat-gift"]/div/div/div/div[2]/div[3]/div[2]/div/input'
            ).send_keys(self.gift_num.get())
        except Exception:
            pass
        self.driver_bank.append(driver)
        self.set_driver_num()

    def quit_one_driver(self):
        if len(self.driver_bank) == 0:
            self.set_tips('无浏览器可退出！')
        else:
            self.driver_bank[-1].quit()
            self.driver_bank.pop()
            self.set_driver_num()

    def divide_driver(self):
        # divide task
        divide_num = 0
        driver_num = len(self.driver_bank)
        self.driver_list = [[], [], [], [], ]
        while divide_num < driver_num:
            for i in range(4):
                self.driver_list[i].append(self.driver_bank[divide_num])
                divide_num += 1
                if divide_num == driver_num:
                    break
        self.set_tips('准备完成,请保证程序置顶,添加浏览器功能关闭')

    def multi_start(self):
        print('multistart')
        p = Pool(5)
        self.qu.put('start')
        # for i in range(4):
        #     print('Assigning')
        #     p.apply_async(self.ready_go, args=(self.driver_list[i], self.qu, ))
        p.apply_async(self.StopGui, args=(self.qu, ))
        p.close()
        p.join()

    # ready for send gift
    def ready_go(self):
        # make sure qu is empty
        while 1:
            if not self.qu.empty():
                self.qu.get()
            else:
                break
        task_bank = []
        # for driver in self.driver_bank:
        for i in range(len(self.driver_bank)):
            task_bank.append(threading.Thread(target=self.wait_signal, args=(self.driver_bank[i], )))
        for task in task_bank:
            task.start()
        for task in task_bank:
            task.join()
        # self.set_tips('准备完成,请保证程序置顶,添加浏览器功能关闭')

    def wait_signal(self, driver):
        send_btn = driver.find_element_by_xpath('//*[@id="LF-chat-gift"]/div/div/div/div[2]/div[3]/a')
        while 1:
            while not self.qu.empty():
                # self.signal.wait()
                send_btn.click()

    def stop_signal(self):
        if not self.qu.empty():
            self.qu.get()
        self.set_tips('结束送礼物')

    def start_signal(self):
        if self.qu.empty():
            self.qu.put('start')
        self.set_tips('开始送礼物')

    def alert_signal(self):
        if self.signal.is_set():
            self.signal.clear()
        else:
            self.signal.set()

    def send_star(self, driver):
        driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[3]/div[3]/div/div/div/div[2]/div[1]/div'
        ).click()
        star = driver.find_element_by_xpath(
                '/html/body/div[1]/div[2]/div[3]/div[3]/div/div/div/div[2]/div[1]/ul/li[2]'
            )
        while 1:
            star.click()
            self.signal.wait()
            print(1)

    def send_one(self):
        if self.driver_bank:
            client = self.driver_bank[0]
            client.find_element_by_xpath(
                '/html/body/div[1]/div[2]/div[3]/div[3]/div/div/div/div[2]/div[3]/a'
            ).click()
        else:
            pass

    def select_gift(self, driver):
        content = driver.page_source
        html = etree.HTML(content)
        try:
            class_content = html.xpath(
                '//*[@id="LF-chat-gift"]/div/div/div/div[1]/div[1]/div/div/div/ul/li[{}]/@class'.format(
                    self.gift_order.get()
                )
            )[0]
        except Exception:
            return True
        if class_content == 'gift selected':
            gift_name = html.xpath(
                '//*[@id="LF-chat-gift"]/div/div/div/div[1]/div[1]/div/div/div/ul/li[{}]/@data-name'.format(
                    self.gift_order.get()
                )
            )[0]
            self.set_tips('登录成功，礼物为：{}，请检查是否选中该礼物'.format(gift_name))
            return False
        else:
            return True

    @staticmethod
    def my_bag_on(driver):
        content = driver.page_source
        html = etree.HTML(content)
        class_content = html.xpath('/html/body/div[1]/div[2]/div[3]/div[3]/div/div/ul/li[4]/@class')[0]
        if class_content == "MR-package on":
            return False
        else:
            return True

    def quit_driver(self):
        if self.driver_bank:
            task_bank = []
            for driver_pat in self.driver_list:
                task_bank.append(threading.Thread(target=self.quit_driver_thread, args=(driver_pat, )))
            for task in task_bank:
                task.start()
            for task in task_bank:
                task.join()
        self.driver_bank = []
        self.driver_list = [[], [], [], [], ]

    @staticmethod
    def quit_driver_thread(driver_list):
        for driver in driver_list:
            driver.quit()


class SubGiftGui(MajorGiftGui):

    def __init__(self, q):
        self.driver = None
        self.signal = threading.Event()
        self.driver_bank = []
        self.cookies_bank = []
        self.driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver.exe')
        self.root = Tk()
        self.root.geometry('460x240')
        self.root.title('副进程')
        self.is_ready = False
        self.qu = q
        self.driver_list = [[], [], [], [], ]
        lb1 = Label(self.root, text='主进程完成登录后使用副进程进行窗口复制')
        lb1.place(relx=0.1, rely=0.01, relwidth=0.8, relheight=0.1)
        lb20 = Label(self.root, text='主播房间号')
        lb20.place(relx=0.01, rely=0.12, relwidth=0.2, relheight=0.1)
        self.room_id = Entry(self.root)
        self.room_id.place(relx=0.23, rely=0.12, relwidth=0.7, relheight=0.1)
        lb30 = Label(self.root, text='刷第几个礼物')
        lb30.place(relx=0.01, rely=0.23, relwidth=0.2, relheight=0.1)
        self.gift_order = Entry(self.root)
        self.gift_order.place(relx=0.23, rely=0.23, relwidth=0.7, relheight=0.1)
        lb4 = Label(self.root, text='每次刷几个')
        lb4.place(relx=0.01, rely=0.34, relwidth=0.22, relheight=0.1)
        self.gift_num = Entry(self.root)
        self.gift_num.place(relx=0.23, rely=0.34, relwidth=0.7, relheight=0.1)
        lb5 = Button(self.root, text='浏览器开启数', command=self.set_driver_num)
        lb5.place(relx=0.01, rely=0.45, relwidth=0.22, relheight=0.1)
        self.driver_num = Entry(self.root)
        self.driver_num.place(relx=0.23, rely=0.45, relwidth=0.7, relheight=0.1)
        btn4 = Button(self.root, text='获得登录信息', command=self.get_login_msg)
        btn4.place(relx=0.05, rely=0.6, relwidth=0.3, relheight=0.2)
        btn5 = Button(self.root, text='复制窗口', command=self.anchor_room)
        btn5.place(relx=0.37, rely=0.6, relwidth=0.3, relheight=0.2)
        btn6 = Button(self.root, text='准备', command=self.ready_go)
        btn6.place(relx=0.68, rely=0.6, relwidth=0.3, relheight=0.2)
        btn8 = Button(self.root, text='退出一个浏览器', command=self.quit_one_driver)
        btn8.place(relx=0.01, rely=0.01, relwidth=0.2, relheight=0.1)
        lb7 = Label(self.root, text='提示')
        lb7.place(relx=0.02, rely=0.89, relwidth=0.1, relheight=0.1)
        self.tip = Entry(self.root)
        self.tip.place(relx=0.13, rely=0.89, relwidth=0.8, relheight=0.1)
        self.root.mainloop()

    def get_login_msg(self):
        if self.qu.empty():
            self.set_tips('没有登录信息，请先完成登录')
            return None
        if self.cookies_bank:
            return None
        else:
            msg = self.qu.get()
        self.cookies_bank = msg[0]
        self.room_id.insert(END, msg[1])
        self.gift_order.insert(END, msg[2])
        self.gift_num.insert(END, msg[3])


class ConGui(MajorGiftGui):

    def __init__(self, q, main_id):
        self.signal = threading.Event()
        self.root = Tk()
        self.root.geometry('400x200')
        self.root.title('控制台大小不一样')
        self.qu = q
        self.main_id = main_id
        lb1 = Label(self.root, text='完成主程序以及副程序的准备后，\n将此程序置顶')
        lb1.place(relx=0.1, rely=0.01, relwidth=0.8, relheight=0.2)
        # btn7 = Button(self.root, text='开始/继续←', command=self.start_signal)
        btn7 = Label(self.root, text='开始/继续←')
        btn7.place(relx=0.1, rely=0.3, relwidth=0.4, relheight=0.2)
        # btn8 = Button(self.root, text='暂停→', command=self.stop_signal)
        btn8 = Label(self.root, text='暂停→')
        btn8.place(relx=0.55, rely=0.3, relwidth=0.4, relheight=0.2)
        btn_convenience = Button(self.root, text='快捷键测试')
        btn_convenience.bind_all('<KeyPress>', self.event_handler, add=True)
        btn_convenience.place()
        lb7 = Label(self.root, text='提示')
        lb7.place(relx=0.02, rely=0.55, relwidth=0.1, relheight=0.15)
        self.tip = Entry(self.root)
        self.tip.place(relx=0.13, rely=0.55, relwidth=0.8, relheight=0.15)
        # btn_start = Button(self.root, text='强制置顶功能开启', command=self.start_top)
        # btn_start.place(relx=0.1, rely=0.75, relwidth=0.15, relheight=0.15)
        # btn_end = Button(self.root, text='暂停/继续强制置顶', command=self.alert_signal)
        # btn_end.place(relx=0.3, rely=0.75, relwidth=0.15, relheight=0.15)
        btn_quit = Button(self.root, text='一键推出', command=self.quit_all)
        btn_quit.place(relx=0.8, rely=0.75, relwidth=0.15, relheight=0.15)
        # self.root.wm_attributes('-topmost', 1)
        self.root.mainloop()

    def quit_all(self):
        command = 'taskkill /F /IM chrome.exe'
        os.system(command)
        command_kill = 'taskkill /pid {}  -t  -f'.format(self.main_id)
        os.system(command_kill)

    # def start_top(self):
    #     self.signal.set()
    #     task_bank = [threading.Thread(target=self.set_top), ]
    #     for task in task_bank:
    #         task.start()
    #     self.set_tips('窗口强制置顶')
    #
    # def set_top(self):
    #     while 1:
    #         print(self.root.wm_focusmodel())
    #         self.signal.wait()
    #         if self.root.wm_focusmodel() != 'passive':
    #             self.root.wm_focusmodel('passive')
    #             print(2)
    #         sleep(0.1)
    #
    # def alert_signal(self):
    #     if self.signal.is_set():
    #         self.signal.clear()
    #         self.set_tips('窗口取消强制置顶')
    #     else:
    #         self.signal.set()
    #         self.set_tips('窗口强制置顶')


if __name__ == '__main__':
    multiprocessing.freeze_support()
    hash_pw = ''
    try:
        with open('./password', 'r') as fh:
            really_pw = fh.read()
    except:
        print('请放置password文件至程序同级目录')
        quit()
    while True:
        pw = getpass.getpass('请输入密码：')
        pw = '{}cms'.format(pw)
        md5 = hashlib.md5()
        md5.update(pw.encode('utf-8'))
        hash_pw = md5.hexdigest()
        if hash_pw == really_pw:
            break
    multi_num = input('请输入进程数，推荐为cpu核数-1，进程数x每个进程网页数=多开数:')
    multi_num = int(multi_num)
    # test id
    # main
    main_pid = os.getpid()
    p = Pool(multi_num + 1)
    que = Manager().Queue(multi_num + 1)
    p.apply_async(MajorGiftGui, args=(que, multi_num))
    for i in range(multi_num - 1):
        p.apply_async(SubGiftGui, args=(que, ))
    p.apply_async(ConGui, args=(que, main_pid, ))
    p.close()
    p.join()