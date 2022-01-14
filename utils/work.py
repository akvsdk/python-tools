# -*- coding: utf8 -*-
import requests
import json
import random
import urllib

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

hitoSimpleApi = 'https://v1.hitokoto.cn/?c=b&encode=text'
hitoApi = 'https://v1.hitokoto.cn/?c=b'
pushApi = 'http://www.pushplus.plus/send?token=42de7fc4d878417fb773dee8062bac10&title=周报小管家&topic=666&template=markdown&content='

json_data = requests.get(url=hitoApi, headers=headers).text

data = json.loads(json_data)
hitokototext = '  ⚡  ' + data['hitokoto'] + '  🦄  ' + data['from']
imgurl = 'https://api.9jojo.cn/acgpic/?rand=' + str(random.randint(100, 999))

content = """# 💥 **周报**              
## 💥 *周报！周报！*        
## 💥 周报！周报！周报！    

🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈🎈


![acg]({})



{}

""".format(imgurl, hitokototext)


def main():
    data = urllib.parse.quote(content, safe='/', encoding=None, errors=None)
    print(data)
    # sendMsg(data)


# 推送给pushplus
def sendMsg(data):
    _result = requests.get(url=pushApi + data, headers=headers).text
    print(_result)


if __name__ == "__main__":
    main()


def main_handler(event, context):
    main()
