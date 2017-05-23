from urllib import request
from lxml import etree
import re
import os
import threadpool
import time
import urllib

_WEBSITE = "http://juren.feiwan.net/manhua/"
_PATH = os.path.join(os.path.abspath('.'), "image")
image_f = None

def checkPath(name):
    if name == "/":
        __path = _PATH
    else:
        __path = os.path.join(_PATH, name)
    if os.path.exists(__path):
        pass
    else:
        os.mkdir(__path)
    return __path


def saveImage(name, image, index):
    print(image)
    # 首先检测下文件夹是否存在
    path = checkPath(name)

    header = {'User-Agent':
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
              "Accept":
                  "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
              "Accept-Encoding": "gzip, deflate, sdch", "Accept-Language": "zh-CN,zh;q=0.8",
              "Cache-Control": "no-cache",
              "Connection": "keep-alive", "Cookie":
                  "__cfduid=d80fb9f1bca182417292e1f1f3da120e11495431247; Hm_lvt_7c51fff13c243b5d978c5336d034017b=1495431247,1495432536; Hm_lpvt_7c51fff13c243b5d978c5336d034017b=1495444021",
              "Upgrade-Insecure-Requests": "1"}
    _image_path = os.path.join(path, str(index) + os.path.splitext(image)[1])
    try:
        req = urllib.request.Request(image, headers=header)
        # request.urlretrieve(image, os.path.join(path, str(index) + os.path.splitext(image)[1]))
        file_object = open(_image_path, 'wb')
        image_f = urllib.request.urlopen(req)
        _body = image_f.read()
        file_object.write(_body)
        file_object.close()

    except BaseException as e:
        print(e)
        time.sleep(0.5)
        os.remove(_image_path)
        if image.endswith(".jpg"):
            saveImage(name, image.replace(".jpg", ".png"), index)

    print("save image " + image)
    pass


def detail(title, link):
    if re.match("http://juren.feiwan.net/manhua/(\d)+.html", _link):
        checkPath(title)

        _curIndex = re.findall("http://juren.feiwan.net/manhua/(\d+).html", _link)[0]
        if int(_curIndex) > 5:
            return

        with request.urlopen(link) as f:
            _html = etree.HTML(f.read().decode("GBK", errors='replace'))
            _pageCount = int(str(_html.xpath("//select/option[last()]/text()")[0]).replace("第", "").replace("页", ""))


            for _pageIndex in range(1, _pageCount):
                _image = "http://img.feiwan.net/juren/manhua/" + _curIndex + "/" + str(_pageIndex) + ".jpg"
                saveImage(title, _image, _pageIndex)


checkPath("/")

with request.urlopen(_WEBSITE) as f:
    _html = etree.HTML(f.read().decode("GBK", errors='replace'))
    _alist = _html.xpath("//a")
    for _a in _alist:
        if len(_a.xpath("text()")) > 0:
            _title = _a.xpath("text()")[0]
            _link = _a.xpath("@href")[0]
            detail(_title, _link)

print("download over")
