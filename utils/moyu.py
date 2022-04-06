import json
from datetime import datetime
import requests
from flask import Flask, jsonify
from loguru import logger
import peewee
from peewee import MySQLDatabase, Model, CharField, TextField, BooleanField, PrimaryKeyField
from playhouse.shortcuts import model_to_dict

holiday_url = "https://api.apihubs.cn/holiday/get?field=year,month,date,holiday&year=2022&holiday_today=1&holiday_legal=1&order_by=1&cn=1&size=31"

db = MySQLDatabase('daily', host='www.941103.xyz', port=3316, user='j1ang', password='66351579')


def create_name(model_class):
    return '纪念日'


class BaseModel(Model):
    class Meta:
        database = db
        table_function = create_name


class Date(BaseModel):
    # 用户名
    id = PrimaryKeyField()
    user = CharField()
    date = TextField()
    text = TextField()
    is_lunar = BooleanField(default=False)


def get_holiday(name):
    r = requests.get(holiday_url)
    state = json.loads(r.text).get('data').get('list')

    result1 = []
    for i in state:
        dt = datetime.strptime(str(i.get('date')), '%Y%m%d')
        result1.append({i.get('holiday_cn'): dt.strftime('%Y-%m-%d')})

    holiday_list = result1
    mine_list = list(Date.select().where(Date.user == name).dicts())
    for i in mine_list:
        if i.get('is_lunar') == 1:
            dt = datetime.strptime(i.get('date'), '%Y-%m-%d')
            lunar_date = date_conversion(datetime.now().year,
                                         dt.month, dt.day)
            holiday_list.append({i.get('text'): lunar_date})
        else:
            dt = datetime.strptime(i.get('date'), '%Y-%m-%d')
            dt.year = datetime.now().year
            holiday_list.append({i.get('text'): dt.strftime('%Y-%m-%d')})

    """
    获取配置中的节日设置
    :return: list——>[{'节日名':'节日日期'}]
    """
    holiday_content = ''
    # 今天日期
    now_str = datetime.now().strftime('%Y-%m-%d')
    now = datetime.strptime(now_str, "%Y-%m-%d")
    logger.info(holiday_list)
    for holiday_info in holiday_list:
        holiday_name = list(holiday_info.keys())[0]
        holiday_date = holiday_info[holiday_name]
        future = datetime.strptime(holiday_date, "%Y-%m-%d")
        if now < future:
            days = (future - now).days
            holiday_content = holiday_content + '距离' + holiday_name + '还有' + str(days) + '天' + '\n'
    return holiday_content


def get_tg():
    """
    获取日记
    :return: bool or str
    """
    url = f"https://fabiaoqing.com/jichou/randomrj.html"
    try:
        res = requests.post(url=url).json()
        return res['tgrj'] + '\n'
    except:
        return False


# 创建表
def create_table(table):
    if not table.table_exists():
        table.create_table()


#     """
#     获取天气预报
#     :return: str or false
#     """
#     url = f"http://apis.juhe.cn/simpleWeather/query"
#     params = {
#         'city': '重庆',
#         'key': '7612ddda2313a41481327cbef5261b46',
#     }
#     try:
#         res = requests.get(url=url, params=params).json()
#         now_str = datetime.datetime.now().strftime('%Y-%m-%d')
#         weather_content = f"""【摸鱼办公室】\n今天是 {now_str} 星期 {datetime.datetime.now().weekday() + 1}\n{res['result']['city']} 当前天气 {res['result']['realtime']['info']} {res['result']['realtime']['temperature']}摄氏度\n早上好，摸鱼人！上班点快到了，收拾收拾，该吃饭吃饭，该溜达溜达，该上厕所上厕所。别闲着\n"""
#         return weather_content
#     except:
#         return False


def date_conversion(year, month, day):
    """
    农历转新历
    :return: str
    """
    url = f"https://www.iamwawa.cn/nongli/api"
    params = {
        'year': year,
        'month': month,
        'day': day,
        'type': 'lunar',
    }
    try:
        user_agent = (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36')
        headers = {'user-agent': user_agent}
        res = requests.get(url=url, params=params, headers=headers).json()
        # logger.info(res)
        dt = datetime.strptime(res['data']['solar'], '%Y年%m月%d日')
        return dt.strftime('%Y-%m-%d')
    except:
        return False


# 节日锚点
mine_list = [
    {"老婆生日": date_conversion(datetime.now().year, 11, 3)},
    {"结婚纪念日": date_conversion(datetime.now().year - 1 if datetime.now().month < 2 else datetime.now().year, 12, 28)},
    {"儿童节": date_conversion(datetime.now().year, 6, 2)},
    # {"老婆生日": "2022-11-26"},
]

app = Flask(__name__)


@app.route('/<name>', methods=['GET'])
def find_api(name=None):
    if not str(name).endswith("ico"):
        return get_daily(name)


def find_name_by_sql(name):
    return list(Date.select().where(Date.user == name).dicts())


@app.route('/add/<name>/<date>/<alias>/<is_lunar>', methods=['GET'])
def add_api(name=None, date=None, alias=None, is_lunar=None):
    """
    :param name: 名字
    :param date: 日期  YYYY-MM-DD
    :param alias:  日期对应别名
    :param is_lunar: 是否是农历
    :return:
    """
    logger.info(f"{name},{date},{alias},{is_lunar}")
    lunar = True if is_lunar == "1" else False
    bean = Date(user=name, date=date, text=alias, is_lunar=lunar)
    bean.save()
    # p1 = Date.select().where(Date.user == 'j1ang').get()
    # model_to_dict(p1)
    p2 = list(Date.select().where(Date.user % '%ang%').dicts())
    logger.info(str(p2))
    return jsonify(p2)


@app.route('/find/<name>', methods=['GET'])
def find_by_name_api(name=None, date=None, alias=None, is_lunar=None):
    res = list(Date.select().where(Date.user == name).dicts())
    return jsonify(res)


@app.route('/favicon.ico')
def favicon():
    # 后端返回文件给前端（浏览器），send_static_file是Flask框架自带的函数
    return "https://cdn.jsdelivr.net/gh/akvsdk/akvsdk.github.io@master/uTools/16367095755421000.png"


def get_daily(name):
    holiday_content = get_holiday(name)
    if not holiday_content:
        logger.error(f"节日为空。")
        holiday_content = ''
    else:
        logger.info(f"获取到节日：\n{holiday_content}")
    tg_content = get_tg()
    if not tg_content:
        logger.error(f"日记为空。")
        tg_content = ''
    else:
        logger.info(f"获取到日记：\n{tg_content}")
    # weather_content = get_weather()
    # if not weather_content:
    #     logger.error(f"天气为空。")
    #     weather_content = ''
    # else:
    #     logger.info(f"获取到天气：\n{weather_content}")
    complete_content = holiday_content + tg_content + '工作再累 一定不要忘记摸鱼哦！有事没事起身去茶水间去厕所去廊道走走，别老在工位上坐着钱是老板的，但命是自己的'
    json = {
        'time': f"""{holiday_content}""",
        'tg': tg_content,
        'c': '工作再累 一定不要忘记摸鱼哦！有事没事起身去茶水间去厕所去廊道走走，别老在工位上坐着钱是老板的，但命是自己的'
    }
    return complete_content


if __name__ == '__main__':
    # holiday_content = get_holiday()
    # if not holiday_content:
    #     logger.error(f"节日为空。")
    #     holiday_content = ''
    # else:
    #     logger.info(f"获取到节日：\n{holiday_content}")
    # tg_content = get_tg()
    # if not tg_content:
    #     logger.error(f"日记为空。")
    #     tg_content = ''
    # else:
    #     logger.info(f"获取到日记：\n{tg_content}")
    # weather_content = get_weather()
    # if not weather_content:
    #     logger.error(f"天气为空。")
    #     weather_content = ''
    # else:
    #     logger.info(f"获取到天气：\n{weather_content}")
    # complete_content = weather_content + holiday_content + tg_content + '工作再累 一定不要忘记摸鱼哦！有事没事起身去茶水间去厕所去廊道走走，别老在工位上坐着钱是老板的，但命是自己的'
    # logger.info(f"整合内容开始推送：\n{complete_content}")
    date = Date()
    create_table(date)
    app.run(host='0.0.0.0', port=1102, threaded=True)
