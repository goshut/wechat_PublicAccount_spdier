import asyncio

# from typing import Optional

import requests
from httpx import Response
from httpx import AsyncClient
from lxml import etree

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "sec-ch-ua-mobile": "?0",
    # "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "referrer": "https://mp.weixin.qq.com/s?__biz=Mzg3NTczMDU2Mg==&mid=2247525137&idx=1&sn=6639d677e9349496bce54a5f79406935&chksm=cf3f20fcf848a9ea95122ce5467d35db05077a26cb4be077c055e211a2f21459c7cfaa5abc7e&token=1528014815&lang=zh_CN&scene=18",
    "referrerPolicy": "strict-origin-when-cross-origin",
    "mode": "cors",
    "credentials": "include",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
}


def get_url_data(url):
    return requests.get(url, headers=headers).text


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
            super().__init__(
                *args,
                headers=kwargs.pop("headers", headers),
                http2=kwargs.pop("http2", True),
                #  follow_redirects=kwargs.pop("follow_redirects", True),
                **kwargs
            )
        AySpider.__has_init = True

    async def get(self, url: str, *args, **kwargs) -> Response:
        """巨坑,,,httpx在发送http协议时有bug,...request能发成功,它不行,必须修改url为https:的形式..
        升级道3.8.10就没这bug了.........
        ############
        这里这样写是为了减少重定向.微信为将他重定向到https的链接
        """
        url = url.replace("http:", "https:", 1)
        return await super().get(url, *args, **kwargs)


if __name__ == "__main__":
    url = "http://mp.weixin.qq.com/s?__biz=Mzg3NTczMDU2Mg==&mid=2247514814&idx=1&sn=61bf8611a69841da0b51669dc2bafbb5&chksm=cf3ff953f8487045a9b5b6cff3d2a7f924fe2ac23b02745d92541d712f2b28f7f01eca20a92d#rd"
    a = AySpider()

    async def tt():
        async with a:
            response = await a.get(url=url)
            print(response.text)
            print("\n" * 3)
            print(response.status_code)
            print(response.headers)
            print(response.http_version)  # HTTP/2

    asyncio.run(tt())
    # res = requests.get(url)
    # print(res.text)
