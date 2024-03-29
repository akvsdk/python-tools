import os
from pygtrans import Translate
import html

"""
阿尔巴尼亚语: sq
阿拉伯语: ar
阿姆哈拉语: am
阿塞拜疆语: az
爱尔兰语: ga
爱沙尼亚语: et
奥利亚语: or
巴斯克语: eu
白俄罗斯语: be
保加利亚语: bg
冰岛语: is
波兰语: pl
波斯尼亚语: bs
波斯语: fa
布尔语(南非荷兰语): af
鞑靼语: tt
丹麦语: da
德语: de
俄语: ru
法语: fr
菲律宾语: tl
芬兰语: fi
弗里西语: fy
高棉语: km
格鲁吉亚语: ka
古吉拉特语: gu
哈萨克语: kk
海地克里奥尔语: ht
韩语: ko
豪萨语: ha
荷兰语: nl
吉尔吉斯语: ky
加利西亚语: gl
加泰罗尼亚语: ca
捷克语: cs
卡纳达语: kn
科西嘉语: co
克罗地亚语: hr
库尔德语: ku
拉丁语: la
拉脱维亚语: lv
老挝语: lo
立陶宛语: lt
卢森堡语: lb
卢旺达语: rw
罗马尼亚语: ro
马尔加什语: mg
马耳他语: mt
马拉地语: mr
马拉雅拉姆语: ml
马来语: ms
马其顿语: mk
毛利语: mi
蒙古语: mn
孟加拉语: bn
缅甸语: my
苗语: hmn
南非科萨语: xh
南非祖鲁语: zu
尼泊尔语: ne
挪威语: no
旁遮普语: pa
葡萄牙语: pt
普什图语: ps
齐切瓦语: ny
日语: ja
瑞典语: sv
萨摩亚语: sm
塞尔维亚语: sr
塞索托语: st
僧伽罗语: si
世界语: eo
斯洛伐克语: sk
斯洛文尼亚语: sl
斯瓦希里语: sw
苏格兰盖尔语: gd
宿务语: ceb
索马里语: so
塔吉克语: tg
泰卢固语: te
泰米尔语: ta
泰语: th
土耳其语: tr
土库曼语: tk
威尔士语: cy
维吾尔语: ug
乌尔都语: ur
乌克兰语: uk
乌兹别克语: uz
西班牙语: es
希伯来语: iw
希腊语: el
夏威夷语: haw
信德语: sd
匈牙利语: hu
修纳语: sn
亚美尼亚语: hy
伊博语: ig
意大利语: it
意第绪语: yi
印地语: hi
印尼巽他语: su
印尼语: id
印尼爪哇语: jw
英语: en
约鲁巴语: yo
越南语: vi
中文（繁体）: zh-TW
中文（简体）: zh-CN
"""

# pip install -U pygtrans

client = Translate(proxies={'http': 'http://192.168.0.220:7890'})


# Translate(proxies={"https": "socks5://localhost:10808"})
def switchLanguage(language):
    with open("./strings.xml") as f:
        lines = f.read().strip()
        f.close()
        filestr = lines.split("\n")
    wf = f'./values-{maps[language]}/'
    if not os.path.exists(wf):
        os.makedirs(wf)
    with open(f'{wf}strings.xml', 'w') as f:
        texts = client.translate(filestr, target=language)
        for x in texts:
            f.write(x.translatedText.replace("&gt;", ">"))  # todo 注意法语的上引号情况
            # f.write(html.unescape(x.translatedText))  # May FIX ？


if __name__ == '__main__':
    maps = {'id': "in-rID", "fr": "fr-rFR", "es": "es-rUS", "pt": "pt-rPT", "ja": "ja-rJP", "it": "it-rIT",
            "nl": "nl-rNL", "ko": "ko-rKR", "tl": "tl-rPH"}
    list = ['ja', 'id', 'fr', 'es', 'pt', 'it', 'ja', 'nl', 'ko', 'tl']
    for lan in list:
        switchLanguage(lan)
