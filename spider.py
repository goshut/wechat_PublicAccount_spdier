import asyncio

import requests
import httpx
from httpx import AsyncClient
from lxml import etree


def get_url_data(url):
    return requests.get(url).text


def get_url_html_tree(url):
    text = get_url_data(url)
    html_tree = etree.HTML(text)
    return html_tree


class AySpider(AsyncClient):
    """对httpx进行全局单列包装"""
    __instance = None
    __has_init = False

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        if not AySpider.__has_init:
            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
                "cache-control": "max-age=0",
                "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "referrer": "https://mp.weixin.qq.com/s?__biz=Mzg3NTczMDU2Mg==&mid=2247525137&idx=1&sn=6639d677e9349496bce54a5f79406935&chksm=cf3f20fcf848a9ea95122ce5467d35db05077a26cb4be077c055e211a2f21459c7cfaa5abc7e&token=1528014815&lang=zh_CN&scene=18",
                "referrerPolicy": "strict-origin-when-cross-origin",
                "mode": "cors",
                "credentials": "include",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            }
            super().__init__(*args, headers=headers, http2=True, **kwargs)
        AySpider.__has_init = True

    async def get(self, **kwargs):
        """巨坑,,,httpx在发送http协议时有bug,...request能发成功,它不行,必须修改url为https:的形式.."""
        if not (_url := kwargs.get('url', None)): return None
        kwargs["url"] = _url.replace("http:", "https:")
        return await super().get(**kwargs)


if __name__ == '__main__':
    url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&action=getalbum&album_id=2516744157244129282#wechat_redirect"
    a = AySpider()


    async def tt():
        async with a:
            res = await a.get(url=url)
            print(res.text)


    asyncio.run(tt())
    # res = requests.get(url)
    # print(res.text)
