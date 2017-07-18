from urllib import request
from lxml import etree
import re
import os
import threadpool
import time

_WEBSITE = "http://www.mzitu.com/all/"
_PATH = os.path.join(os.path.abspath('.'), "image")


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
    # 首先检测下文件夹是否存在
    path = checkPath(name)
    request.urlretrieve(image, os.path.join(path, str(index) + os.path.splitext(image)[1]))
    print("save image " + image)
    # request.urlretrieve(image, os.path.join(_PATH, name + "-" + str(index) + os.path.splitext(image)[1]))
    pass


def parseDetail(name, link, index):
    if not (re.match("http://www.mzitu.com[/(\d)]+$", link)):
        return None
    if link == "http://www.mzitu.com/":
        return None
    try:
        with request.urlopen(link) as f:
            _html = etree.HTML(f.read().decode("UTF-8"))
            _image = _html.xpath("//div[@class='main-image']//img/@src")[0]
            _nextLink = _html.xpath("//div[@class='pagenavi']/a[last()]/@href")[0]
            # 保存图片
            saveImage(name, _image, index)
            if re.match("http://www.mzitu.com/(\d)+$", _nextLink):
                return None
            parseDetail(name, _nextLink, index + 1)
    except BaseException as e:
        print(e)
        time.sleep(0.5)
        parseDetail(name, link, index)


# 首先检测下根目录是否存在
checkPath("/")

with request.urlopen(_WEBSITE) as f:
    _data = f.read()
    _html = etree.HTML(_data.decode("UTF-8"))
    _alist = _html.xpath("//a")
    pool = threadpool.ThreadPool(30)
    requests = []
    for _a in _alist:
        _name = _a.xpath("text()")
        _link = _a.xpath("@href")
        if len(_name) == 1:
            args_list = []
            args_list.append(_name[0])
            args_list.append(_link[0])
            args_list.append(0)
            requests.append(threadpool.makeRequests(parseDetail, [((_name[0], _link[0], 0), {})])[0])
    [pool.putRequest(req) for req in requests]
    pool.wait()
    # parseDetail(_name[0], _link[0], 0)

print("over....")
