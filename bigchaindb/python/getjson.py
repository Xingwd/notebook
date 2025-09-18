import urllib
import json

def getJson(url):

    # 通过urllib模块中的urlopen的方法打开url
    urlinfo = urllib.request.urlopen(url)
    # 获取url信息
    info = urlinfo.read()

    return json.loads(info)

'''
url = "http://www.redoop.com/xingliannong/teaIndex"
teainfo = getJson(url)
for i in teainfo:
    i.pop('id')
    print(i)
'''


