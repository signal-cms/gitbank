import os
import time
from time import sleep
import threading
from tkinter import *
from tkinter import messagebox
from selenium import webdriver
from lxml import etree
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from multiprocessing import Manager


# class NewAction(ActionChains):
#
#     pass


class GiftGui:

    def __init__(self):
        self.driver = None
        self.signal = threading.Event()
        self.driver_bank = []
        self.cookies_bank = []
        self.driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver.exe')
        self.root = Tk()
        self.root.geometry('460x240')
        self.root.title('刷礼物多开器')
        self.is_ready = False
        lb1 = Label(self.root, text='填写信息，点击启动后开始自动刷取')
        lb1.place(relx=0.1, rely=0.01, relwidth=0.8, relheight=0.1)

        lb20 = Label(self.root, text='主播房间号')
        lb20.place(relx=0.01, rely=0.12, relwidth=0.2, relheight=0.1)
        self.room_id = Entry(self.root)
        self.room_id.place(relx=0.23, rely=0.12, relwidth=0.3, relheight=0.1)
        # lb21 = Label(self.root, text='多开数')
        # lb21.place(relx=0.53, rely=0.12, relwidth=0.15, relheight=0.1)
        # self.thread_num = Entry(self.root)
        # self.thread_num.place(relx=0.68, rely=0.12, relwidth=0.3, relheight=0.1)

        lb30 = Label(self.root, text='刷第几个礼物')
        lb30.place(relx=0.01, rely=0.23, relwidth=0.2, relheight=0.1)
        self.gift_order = Entry(self.root)
        self.gift_order.place(relx=0.23, rely=0.23, relwidth=0.3, relheight=0.1)
        # lb31 = Label(self.root, text='刷几次')
        # lb31.place(relx=0.53, rely=0.23, relwidth=0.15, relheight=0.1)
        # self.gift_time = Entry(self.root)
        # self.gift_time.place(relx=0.68, rely=0.23, relwidth=0.3, relheight=0.1)

        lb4 = Label(self.root, text='每次刷几个')
        lb4.place(relx=0.01, rely=0.34, relwidth=0.22, relheight=0.1)
        self.gift_num = Entry(self.root)
        self.gift_num.place(relx=0.23, rely=0.34, relwidth=0.3, relheight=0.1)
        # lb5 = Label(self.root, text='刷手账号')
        # lb5.place(relx=0.01, rely=0.45, relwidth=0.2, relheight=0.1)
        # self.user_id = Entry(self.root)
        # self.user_id.place(relx=0.23, rely=0.45, relwidth=0.3, relheight=0.1)
        # lb6 = Label(self.root, text='刷手密码')
        # lb6.place(relx=0.01, rely=0.56, relwidth=0.2, relheight=0.1)
        # self.password = Entry(self.root)
        # self.password.place(relx=0.23, rely=0.56, relwidth=0.3, relheight=0.1)

        btn9 = Button(self.root, text='一键退出', command=self.quit_driver)
        btn9.place(relx=0.6, rely=0.2, relwidth=0.3, relheight=0.3)

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
        btn7 = Button(self.root, text='开始/继续←', command=self.start_signal)
        btn7.place(relx=0.52, rely=0.78, relwidth=0.2, relheight=0.1)
        btn8 = Button(self.root, text='暂停→', command=self.stop_signal)
        btn8.place(relx=0.78, rely=0.78, relwidth=0.2, relheight=0.1)
        lb7 = Label(self.root, text='提示')
        lb7.place(relx=0.02, rely=0.89, relwidth=0.1, relheight=0.1)
        btn_convenience = Button(self.root, text='快捷键测试')
        btn_convenience.bind_all('<KeyPress>', self.event_handler)
        btn_convenience.place()
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
        self.driver = webdriver.Chrome(executable_path=self.driver_path)
        self.driver.implicitly_wait(3)
        # login page
        self.driver.get(
            'https://cnpassport.laifeng.com/mini_login.htm?lang=zh_cn&appName=youku&appEntrance=laifeng&styleType='
            'vertical&bizParams=&notLoadSsoView=true&notKeepLogin=false&isMobile=false&pid=20160918PLF000695&rnd='
            '0.7248185733783202')
        # driver.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(self.user_id.get())
        # driver.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(self.password.get())
        # sleep(0.1)
        # driver.find_element_by_xpath('/html/body/div[1]/div/div/div/form/div[6]/button').click()
        # sleep(2)
        # anchor page
        # self.driver.get('https://www.laifeng.com/')
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
        self.set_tips('获取登录信息成功,请测试')

    def gift_test(self):
        if not self.cookies_bank:
            self.set_tips('请按完成登录,获取登录信息后再进行测试')
            return None
        if self.room_id.get():
                self.driver.get('https://v.laifeng.com/{}'.format(self.room_id.get()))
                sleep(1)
                # click my bag until on
                # while self.my_bag_on(driver):
                #     driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[3]/div/div/ul/li[4]').click()
                # click until special gift is selected
                # select gift
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

    @staticmethod
    def set_gift_num( driver):
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

    # def thread_driver(self):
    #     task_bank = []
    #     if not self.thread_num.get():
    #         self.set_tips('请输入多开数!')
    #         return None
    #     else:
    #         self.driver.quit()
    #     task_num = int(self.thread_num.get())
    #     for i in range(task_num):
    #         task_bank.append(threading.Thread(target=self.copy_driver))
    #     for task in task_bank:
    #         task.start()
    #     for task in task_bank:
    #         task.join(timeout=8)
    #     self.set_tips('登录完成,请检查登录状态,礼物是否异常,若异常,请手动修正!')

    def copy_driver(self):
        if not self.cookies_bank:
            self.set_tips('请按完成登录,获取登录信息后再进行复制窗口')
            return None
        driver = webdriver.Chrome(executable_path=self.driver_path)
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
        if not self.driver_bank:
            self.driver_bank.append(self.driver)
        self.driver_bank.append(driver)

    # ready for send gift
    def ready_go(self):
        self.signal.clear()
        task_bank = []
        # for driver in self.driver_bank:
        for i in range(len(self.driver_bank)):
            task_bank.append(threading.Thread(target=self.wait_signal, args=(self.driver_bank[i], )))
        for task in task_bank:
            task.start()
        self.set_tips('准备完成,请保证程序置顶,添加浏览器功能关闭')

    def wait_signal(self, driver):
        send_btn = driver.find_element_by_xpath('//*[@id="LF-chat-gift"]/div/div/div/div[2]/div[3]/a')
        while True:
            self.signal.wait()
            send_btn.click()
        # print(num, ct)

    def stop_signal(self):
        self.signal.clear()
        self.set_tips('暂停送礼')

    def start_signal(self):
        self.signal.set()
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
        while True:
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
            for driver in self.driver_bank:
                driver.quit()
        self.driver_bank = []


if __name__ == '__main__':
    try:
        gift = GiftGui()
    except Exception as err:
        messagebox.showerror(title='出错啦！', message=str(err))