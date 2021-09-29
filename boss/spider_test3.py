import requests
import re
from selenium import webdriver
from scrapy import Selector
import pymysql.cursors
import time
import re
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from peewee import *

db = MySQLDatabase('spider', host='ml.j1ang.xyz', port=3306,
                   user='j1ang', password='123456')


class BaseModel(Model):
    class Meta:
        database = db
        table_name = 'spider'


class Data(BaseModel):
    url = TextField(default='')
    content = TextField(default='')
    primary = TextField(default='')
    needs = TextField(default='')
    place = TextField(default='')
    company = TextField(default='')
    welfare = TextField(default='')
    create_data = DateField(formats=['%d-%b-%Y %H:%M:S%'])


connection = pymysql.connect(host='ml.j1ang.xyz',
                             user='j1ang',
                             password='123456',
                             database='spider',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def getStrName():
    name = '重庆'
    if name.isspace():
        name = input('\n输入城市名:')
        return name
    else:
        return name


def getStrSearch():
    search = 'android'
    if search.isspace():
        search = input('\n输入要搜索的职位:')
        return search
    else:
        return search


cityname = getStrName()

search = getStrSearch()


def get_boss_info():
    city_url = 'https://www.zhipin.com/wapi/zpgeek/common/data/citysites.json'
    res = requests.get(city_url).text
    pattern = re.compile(r'"name":"(.*?)","code":(.*?),')
    datas = re.findall(pattern, res)
    # print(datas)
    data_dict = {}
    for i in datas:
        name, code = i
        data_dict[name] = code
        print(i[0] + '\t', end='')
    print(data_dict)
    print('\n'+cityname)
    print('\n'+data_dict[cityname])
    url_temp = 'https://www.zhipin.com/c{}/?query={}'.format(
        data_dict[cityname], search)
    return url_temp


def xpath_get_data(sel, xpath):
    if len(sel.xpath(xpath)) != 0:
        return sel.xpath(xpath).extract()[0]
    else:
        return ''


def table_exists(con, name):
    sql = 'show tables;'
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        return 1  # 存在返回1
    else:
        return 0  # 不存在返回0


def insert_data():
    sql = "INSERT INTO `data` (`url`, `content`, `primary`,`needs`,`place`,`company`,`welfare`) VALUES (%s, %s, " \
        "%s, %s, %s, %s, %s)"
    for i in tag:
        cursor.execute(sql, (i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
        connection.commit()
        cursor.close()
        end_time = time.time()
        print('runtime:{}'.format(end_time - begin_time))


def create_data():
    sql = "CREATE DATABASE `spider` CHARACTER SET 'utf8mb4';"
    cursor.execute(sql)
    insert_data()


# 不显示浏览器
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(
    'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
if __name__ == '__main__':
    url_temp = get_boss_info()
    begin_time = time.time()
    db.create_tables([Data])
    url_temp_head = 'https://www.zhipin.com'
    tag = []
    StopFlag = True
    browser = webdriver.Chrome(options=chrome_options)
    i = 1
    while StopFlag:
        if i == 1:
            print(url_temp)
            browser.get(url_temp)
        else:
            normal_window = browser.current_window_handle
        time.sleep(0.5)
        temp = browser.page_source
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
                url.append(xpath_get_data(sel,
                                          '//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[1]/div[1]/div/div[1]/span[1]/a/@href'.format(
                                              k)))
                content.append(xpath_get_data(sel,
                                              '//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[1]/div[1]/div/div[1]/span['
                                              '1]/a/text()'.format(
                                                  k)))
                primary.append(xpath_get_data(sel,
                                              '//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[1]/div[1]/div/div[2]/span/text()'.format(
                                                  k)))
                needs.append(
                    xpath_get_data(sel,
                                   '//*[@id="main"]/div/div[3]/ul/li/div/div[1]/div[1]/div/div[2]/p/text()'.format(k)))
                place.append(xpath_get_data(sel,
                                            '//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[1]/div[1]/div/div[1]/span['
                                            '2]/span/text()'.format(
                                                k)))
                company.append(
                    xpath_get_data(sel,
                                   '//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[1]/div[2]/div/h3/a/text()'.format(k)))
                welfare.append(
                    xpath_get_data(sel, '//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[2]/div[2]/text()'.format(k)))
        else:
            for k in range(1, 31):
                temp_url = xpath_get_data(sel,
                                          '//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[1]/div[1]/div/div[1]/span[1]/a/@href'.format(
                                              k))
                if len(temp_url) == 0:
                    StopFlag = False
                    break
                url.append(temp_url)
                content.append(xpath_get_data(sel,
                                              '//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[1]/div[1]/div/div[1]/span['
                                              '1]/a/text()'.format(
                                                  k)))
                primary.append(xpath_get_data(sel,
                                              '//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[1]/div[1]/div/div[2]/span/text()'.format(
                                                  k)))
                needs.append(
                    xpath_get_data(sel,
                                   '//*[@id="main"]/div/div[2]/ul/li/div/div[1]/div[1]/div/div[2]/p/text()'.format(k)))
                place.append(xpath_get_data(sel,
                                            '//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[1]/div[1]/div/div[1]/span['
                                            '2]/span/text()'.format(
                                                k)))
                company.append(
                    xpath_get_data(sel,
                                   '//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[1]/div[2]/div/h3/a/text()'.format(k)))
                welfare.append(
                    xpath_get_data(sel, '//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[2]/div[2]/text()'.format(k)))
        for n in range(0, len(url)):
            # tag.append([url_temp_head + url[n], content[n], primary[n],
            #            needs[n], place[n], company[n], welfare[n]])
            tag.append(Data(url=url_temp_head + url[n], content=content[n], primary=primary[n], needs=needs[n], place=place[n],
                       company=company[n], welfare=welfare[n], create_data=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
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
    with db.atomic():
        Data.delete().execute()
        Data.bulk_create(tag)
        end_time = time.time()
        print('runtime:{}'.format(end_time - begin_time))

    # with connection:
    #     with connection.cursor() as cursor:
    #         sql = "INSERT INTO `data` (`url`, `content`, `primary`,`needs`,`place`,`company`,`welfare`,`create_data`) VALUES (%s, %s, "
    #               "%s, %s, %s, %s, %s, NOW()) "
    #         for i in tag:
    #             cursor.execute(sql, (i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
    #             connection.commit()
    #         cursor.close()
    #         end_time= time.time()
    #         print('runtime:{}'.format(end_time - begin_time))
