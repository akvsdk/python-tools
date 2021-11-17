import requests
import pandas as pd
from datetime import date

data = []


def getIp(size):
    for i in range(size):
        r = requests.get('http://10.211.55.4:5555/random')
        data.append(r.text)


def checkUse(ipaddress):
    iplist = []
    for ip in ipaddress:
        try:
            proxy = {
                'http': 'http://%s' % ip
            }
            '''head 信息'''
            head = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                'Connection': 'keep-alive'}
            '''http://icanhazip.com会返回当前的IP地址'''
            p = requests.get('http://icanhazip.com', headers=head, proxies=proxy)
            print(p.text)
            if p.text in ip:
                iplist.append(ip)
                print("check success:" + p.text)
        except:
            print("check error:" + ip)
    return iplist

def checkUse2(ipaddress):
    iplist = []
    for ipad in ipaddress:
        try:
            url = "http://www.baidu.com/"
            strlist = ipad.split(':')
            ip, port = strlist[0], strlist[1]
            proxies = {"http": f"http://{ip}:{port}"}
            # 空白位置为测试代理ip和代理ip使用端口
            head = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                'Connection': 'keep-alive'}
            # 响应头
            res = requests.get(url, proxies=proxies, headers=head)
            # 发起请求
            if res.status_code==200:
                iplist.append(ipad)
                print("check ok:" + ipad)
            else:
                print(res.status_code)  # 返回响应码
        except:
            print("check error:" + ip)
    return iplist

def writeipfile(lst2):
    now = date.today().strftime("%y_%m_%d")
    for i in lst2:
        with open('getproxy_%s.txt' % now, 'a+') as f:  # 设置文件对象
            f.write(i + '\n')  # 将字符串写入文件中


if __name__ == '__main__':
    getIp(300)
    lst = {}.fromkeys(data).keys()
    lst2 = checkUse2(lst)
    writeipfile(lst2)
