import os
import xlwt
from selenium import webdriver
from lxml import etree
from time import sleep
import traceback
import warnings
import sys


def command_line(driver, tip='请输入指令(1登录/2爬取/3退出,回车确定):'):
    cmd = input(tip)
    if cmd == '登录' or cmd == '1':
        login_in(driver)
    elif cmd == '爬取' or cmd == '2':
        spider(driver)
    elif cmd == '退出' or cmd == '3':
        driver.quit()
    else:
        command_line(driver, '无效指令，请重新输入指令(1登录/2爬取/3退出,回车确定):')


def login_in(driver):
    driver.get('https://www.laifeng.com/')
    command_line(driver, '已打开登录界面，登录完成后输入 2爬取，进行爬取')


def spider(driver):
    driver.get('https://v.laifeng.com/my/consumerecord?spm=a2h55.10574706.UC-left-menu-hook.3!2~1~3!2~A&pageNo=1')
    content = driver.page_source
    html = etree.HTML(content)
    try:
        ttl_page = int(html.xpath('/html/body/div[4]/div/div[2]/div/span[@class="dds-pager-page"]/text()')[-1])
    except IndexError:
        ttl_page = 1
    user_name = html.xpath('/html/body/div[3]/div/div[1]/div[2]/div[1]/span/text()')[0]
    msg = []
    for i in range(1, ttl_page+1):
        driver.get(
            'https://v.laifeng.com/my/consumerecord?spm=a2h55.10574706.UC-left-menu-hook.3!2~1~3!2~A&pageNo={}'.format(
                i
            )
        )
        sleep(0.5)
        content = driver.page_source
        msg.append(get_msg(content))
    writer(msg, user_name, driver)


def writer(msg, name, driver):
    # sort data
    data = []
    for info in msg:
        for i in range(len(info)//3):
            data.append(info[i*3:(i+1)*3])
    # add room id
    # add user name
    for i in range(len(data)):
        data[i].append(name)
    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    wb = xlwt.Workbook(encoding='utf-8')
    sh = wb.add_sheet('消费记录')
    for i in range(len(data)):
        for j in range(len(data[i])):
            sh.write(i, j, data[i][j])
    wb.save('{}.xls'.format(file_name))
    command_line(driver)


def get_msg(content):
    html = etree.HTML(content)
    msg = html.xpath('/html/body/div[4]/div/table/tbody/tr/td/text()')
    return msg


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver.exe')
    driver = webdriver.Chrome(executable_path=driver_path)
    try:
        command_line(driver)
    except Exception as err:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.txt'), 'a') as fh:
            fh.write(err)
            for i in range(3):
                fh.write(str(sys.exc_info()[i]))
