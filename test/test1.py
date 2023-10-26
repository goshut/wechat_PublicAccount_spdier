import json

import requests
from lxml import etree

URL = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&action=getalbum&album_id=2206970536067497985&scene=173&from_msgid=2247493173&from_itemidx=1&count=3&nolastread=1#wechat_redirect"
ROLL_URL = "https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&__biz=Mzg3NTczMDU2Mg==&album_id=2206970536067497985&count=10&begin_msgid={begin_msgid}&begin_itemidx=1&uin=&key=&pass_ticket=&wxtoken=&devicetype=&clientversion=&__biz=Mzg3NTczMDU2Mg%3D%3D&appmsg_token=&x5=0&f=json"

# response = requests.get(url=URL)
# text = response.text
# html_tree = etree.HTML(text)
xpath = "//li[@class='album__list-item js_album_item js_wx_tap_highlight wx_tap_cell']"
dir_name_xpath = '//div[@id="js_tag_name"]/text()'

# data = html_tree.xpath(xpath)[0]
# # print(etree.tounicode(data, method="html"))
# print(data.attrib["data-msgid"])
# print(data.attrib["data-title"])

articleurl = []
dir_name = ''


def get_articleurl_list(wxset_url):
    # 第一次构建
    response = requests.get(url=wxset_url)
    text = response.text
    html_tree = etree.HTML(text)
    dir_name = html_tree.xpath(dir_name_xpath)[0]
    print(dir_name)
    data = html_tree.xpath(xpath)[0]
    first_begin_msgid = data.attrib["data-msgid"]
    articleurl.append(data.attrib["data-link"])
    # get_roll_json(first_begin_msgid)


def get_roll_json(begin_msgid):
    response = requests.get(url=ROLL_URL.format(begin_msgid=begin_msgid))
    text = response.text
    roll_json = json.loads(text)
    # print(roll_json)
    # 如果roll_json['base_resp']['ret']为-1表示url错误,返回一个错误码
    if roll_json['base_resp']['ret'] == -1:
        return -1
    # 如果有结果
    next_begin_msgid = 0
    if article_list := roll_json["getalbum_resp"].get('article_list', 0):
        # 如果是list的情况
        if type(article_list) is list:
            # print(roll_json["getalbum_resp"]["article_list"][0]["url"])
            [articleurl.append(i["url"]) for i in article_list]
            # print(articleurl)
            next_begin_msgid = article_list[-1]['msgid']
        # 如果是dict的情况
        elif type(article_list) is dict:
            articleurl.append(article_list['url'])
            next_begin_msgid = article_list['msgid']
    # 没有了结束
    else:
        return 0
    get_roll_json(next_begin_msgid)


if __name__ == '__main__':
    get_articleurl_list(URL)
    print(articleurl)
