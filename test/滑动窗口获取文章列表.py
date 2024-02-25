import httpx, requests
from time_code import *
import requests

method = "GET"
url = "https://mp.weixin.qq.com/mp/appmsgalbum"
params = {
    "action": "getalbum",
    "__biz": "Mzg3NTczMDU2Mg==",
    "album_id": "2413802396947742721",
    "count": "30",
    "begin_msgid": "2247524660",
    "begin_itemidx": "2",
    "uin": "",
    "key": "",
    "pass_ticket": "",
    "wxtoken": "",
    "devicetype": "",
    "clientversion": "",
    "appmsg_token": "",
    "x5": "0",
    "f": "json"
}
headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    "referrer": "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&action=getalbum&album_id=2413802396947742721",
    "referrerPolicy": "strict-origin-when-cross-origin",
    "mode": "cors",
    "credentials": "include",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}
# response = requests.request(method, url, params=params, headers=headers)
# print(response.text)

@timed
def t():
    response = requests.request(method, url, params=params, headers=headers)
    print(response.text)
    json_data = response.json()
    print(len(json_data["getalbum_resp"]["article_list"]))


@timed
def t1():
    response = httpx.request(method, url, params=params, headers=headers)
    # print(response.json())
    res_json = response.json()
    for i in (article_list := res_json["getalbum_resp"]["article_list"]):
        print(i)
    print(len(article_list))


@timed
def t2():
    response = requests.request(method, url, params=params, headers=headers)
    # print(response.json())
    res_json = response.json()
    for i in (article_list := res_json["getalbum_resp"]["article_list"]):
        print(i)
    print(len(article_list))


if __name__ == '__main__':
    t()
    # t1()
    # t2()
