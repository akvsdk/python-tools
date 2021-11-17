import requests
import re
from selenium import webdriver
from scrapy import Selector
import time
from peewee import Database, TextField, MySQLDatabase, Model, IntegerField
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import pandas as pd
import csv
import json


# 基本变量
# 搜索地址请求地址
city_url = 'https://www.zhipin.com/wapi/zpgeek/common/data/citysites.json'
# 搜索地址数组
data_dict = {}
# 搜索的默认地址
name = '福州'
# 搜索的默认职业
search = 'Android'
# 防止检测生成的cookies
cookies = ''
# 爬出数据
source = []
# 爬取开始时间
begin_time = time.time()

# 前置城市查询
def findCityData():
    res = requests.get(city_url).text
    pattern = re.compile(r'"name":"(.*?)","code":(.*?),')
    datas = re.findall(pattern, res)
    for i in datas:
        name, code = i
        data_dict[name] = code
        print(i[0] + '\t', end='')


# 做一个域到cookie的映射
def getPureDomainCookies(cookies):
    domain2cookie = {}
    for cookie in cookies:
        domain = cookie['domain']
        if domain in domain2cookie:
            domain2cookie[domain].append(cookie)
        else:
            domain2cookie[domain] = []
    maxCnt = 0
    ansDomain = ''
    for domain in domain2cookie.keys():
        cnt = len(domain2cookie[domain])
        if cnt > maxCnt:
            maxCnt = cnt
            ansDomain = domain
    ansCookies = domain2cookie[ansDomain]
    return ansCookies

# 读取本地Cookie
def getCookie():
    with open('cookie.txt', 'r') as f:
        cookies = json.load(f)
    cookies = getPureDomainCookies(cookies)

    # if len(name)==0:
    #     return input('\n输入要搜索的城市:')
    # else:
    #     return name

# 前置职位获取
# def findCitySearch():
# if len(search)==0:
#     return input('\n输入要搜索的职位:')
# else:
#     return search


# 职位搜索
# def findCitySearch():
# if len(search)==0:
#     return input('\n输入要搜索的职位:')
# else:
#     return search


# 生成本地Cookie
# class getCookie:
#     def main(self, url):
#         option = webdriver.ChromeOptions()
#         option.add_argument(r'--user-data-dir=C:\Users\70769\AppData\Local\Google\Chrome\User Data')
#         option.add_argument(r'--profile-directory=Default')
#         browser = webdriver.Chrome(options=option)
#         browser.get(url)
#         browser.implicitly_wait(60)
#         time.sleep(20)
#         try:
#             # 获取登陆成功后的cookie信息
#             login_rear_cookie = browser.get_cookies()
#             if login_rear_cookie:
#                 # 把cookie信息用json序列化后写入cookie.txt文件
#                 with open('cookie.txt', 'w') as f:
#                     f.write(json.dumps(login_rear_cookie))
#                 print('获取cookie信息成功')
#         except Exception as e:
#             print('获取cookie失败:{}'.format(e))
#         finally:
#             browser.quit()
# if __name__ == '__main__':
#     url = "https://www.zhipin.com/c101230100/?query=%E9%87%8D%E5%BA%86"
#     st = getCookie()
#     st.main(url)


# xpath 取数据
def xpath_get_data(sel, xpath):
    if len(sel.xpath(xpath)) != 0:
        return sel.xpath(xpath).extract()[0]
    else:
        return ''


def openWebGetData():
    url_temp = 'https://www.zhipin.com/c{}/?query={}'.format(data_dict[name], search)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
    chrome_options.add_argument('--disable-gpu')
    begin_time = time.time()
    id = 1
    url_temp_head = 'https://www.zhipin.com'
    StopFlag = True
    browser = webdriver.Chrome(options=chrome_options, executable_path="./chromedriver")
    browser.implicitly_wait(10)
    i = 1
    while StopFlag:
        if i == 1:
            browser.get(url_temp)
            time.sleep(0.5)
        else:
            normal_window = browser.current_window_handle
        temp = browser.page_source
        for cookie in cookies:
            browser.add_cookie(cookie)
        sel = Selector(text=temp)
        url = []
        content = []
        primary = []
        needs = []
        place = []
        company = []
        welfare = []
        if i == 1:
            for k in range(1, 31):
                url = xpath_get_data(sel,
                                     '//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[1]/div[1]/div/div[1]/span[1]/a/@href'.format(
                                         k))
                content = xpath_get_data(sel,
                                         '//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[1]/div[1]/div/div[1]/span['
                                         '1]/a/text()'.format(
                                             k))
                primary = xpath_get_data(sel,
                                         '//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[1]/div[1]/div/div[2]/span/text()'.format(
                                             k))
                needs = xpath_get_data(sel,
                                       '//*[@id="main"]/div/div[3]/ul/li/div/div[1]/div[1]/div/div[2]/p/text()'.format(
                                           k))
                place = xpath_get_data(sel,
                                       '//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[1]/div[1]/div/div[1]/span['
                                       '2]/span/text()'.format(
                                           k))
                company = xpath_get_data(sel,
                                         '//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[1]/div[2]/div/h3/a/text()'.format(
                                             k))
                welfare = xpath_get_data(
                    sel, '//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[2]/div[2]/text()'.format(k))
                source.append([url_temp_head + url, content, primary,
                               needs, place, company, welfare])

        else:
            for k in range(1, 31):
                temp_url = xpath_get_data(sel,
                                          '//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[1]/div[1]/div/div[1]/span[1]/a/@href'.format(
                                              k))
                if len(temp_url) == 0:
                    StopFlag = False
                    break
                url = temp_url
                content = xpath_get_data(sel,
                                         '//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[1]/div[1]/div/div[1]/span['
                                         '1]/a/text()'.format(
                                             k))
                primary = xpath_get_data(sel,
                                         '//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[1]/div[1]/div/div[2]/span/text()'.format(
                                             k))
                needs = xpath_get_data(sel,
                                       '//*[@id="main"]/div/div[2]/ul/li/div/div[1]/div[1]/div/div[2]/p/text()'.format(
                                           k))
                place = xpath_get_data(sel,
                                       '//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[1]/div[1]/div/div[1]/span['
                                       '2]/span/text()'.format(
                                           k))
                company = xpath_get_data(sel,
                                         '//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[1]/div[2]/div/h3/a/text()'.format(
                                             k))
                welfare = xpath_get_data(
                    sel, '//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[2]/div[2]/text()'.format(k))
                source.append([url_temp_head + url, content, primary,
                               needs, place, company, welfare])
        if StopFlag == False:
            print('complete {}'.format(i))
            break
        try:
            click_ele = browser.find_element_by_xpath('//*[@class="next"]')
            click_ele.click()
        except NoSuchElementException as e:
            StopFlag = False
            break
        finally:
            print('complete {}'.format(i))
        i += 1
    browser.close()

# 生成最后数据
def writeDataToDb():
    df = pd.DataFrame(data=source, columns=[
        '网址', '职位', '薪水', '需求', '地点', '公司', '福利'])
    df = df.set_index('网址')
    df.to_csv('{}_{}_{}.csv'.format(name, search, time.strftime(
        "%Y-%m-%d", time.localtime())), index=True, encoding='utf_8_sig')
    end_time = time.time()
    print('runtime:{}'.format(end_time - begin_time))


if __name__ == '__main__':
    findCityData()
    getCookie()
    openWebGetData()
    writeDataToDb()

