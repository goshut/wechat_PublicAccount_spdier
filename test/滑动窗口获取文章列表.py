import httpx, requests
from time_code import *

method = "GET"
url = "https://mp.weixin.qq.com/mp/appmsgalbum"
params = {
    "__biz": "Mzg3NTczMDU2Mg==",
    "action": "getalbum",
    "album_id": "2608550406499041280",
    "scene": "21"
}
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "referrerPolicy": "strict-origin-when-cross-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}
cookies = {
    "pgv_pvid": "2448401297",
    "pgv_pvi": "7457755136",
    "RK": "1NzorZpzYG",
    "ptcz": "9697e3741ba546da731dfde7740bd7c04fc8cb3d30c55be16a8e0954c2a5d3c3",
    "tvfe_boss_uuid": "26942402fdcc64ae",
    "pac_uid": "1_952918451",
    "iip": "0",
    "fqm_pvqid": "06ad7011-2b16-4933-b98c-5c256add73e6",
    "gr_user_id": "65d1cd3a-f20f-431b-8fd4-6ec83d114366",
    "ua_id": "TFIILZLR9TAFwcyqAAAAANoaYF-cx23dWMuiQjqdbnE",
    "wxuin": "78699844319951",
    "qq_domain_video_guid_verify": "987821355383c532",
    "ptui_loginuin": "952918451@qq.com"
}


@timed
def t():
    response = requests.request(method, url, params=params, headers=headers, cookies=cookies)
    print(response.text)


@timed
def t1():
    response = httpx.request(method, url, params=params, headers=headers, cookies=cookies)
    # print(response.json())
    res_json = response.json()
    for i in (article_list := res_json["getalbum_resp"]["article_list"]):
        print(i)
    print(len(article_list))


@timed
def t2():
    response = requests.request(method, url, params=params, headers=headers, cookies=cookies)
    # print(response.json())
    res_json = response.json()
    for i in (article_list := res_json["getalbum_resp"]["article_list"]):
        print(i)
    print(len(article_list))


if __name__ == '__main__':
    t()
    # t1()
    # t2()
