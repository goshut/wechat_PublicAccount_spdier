import asyncio

import httpx
from httpx import Response
from time_code import *

c = httpx.AsyncClient()


class TC(httpx.AsyncClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         # headers=kwargs.pop("headers", headers),
                         http2=kwargs.pop("http2", True),
                         follow_redirects=kwargs.pop("follow_redirects", True),
                         **kwargs)

    async def get(self, *args, **kwargs) -> Response:
        return await super().get(*args, **kwargs)


tc = TC()


async def get_data():
    async with tc:
        with CodeTimer():
            res = await tc.get("http://127.0.0.1:9999/welcome/<name>")
        print(res.text)
        print(res.status_code)
        print(res.headers)
        print(res.http_version)
        print(res.history)


def a(q, w, *args, **kwargs):
    print(q, w)
    print(args)
    print(kwargs)


def b(q, w, *args, **kwargs):
    a(q, w, 636, *args,
      ss=kwargs.pop("ss", "zxc"),
      **kwargs,
      )


if __name__ == '__main__':
    with CodeTimer():
        asyncio.run(get_data())
    # b(123, 456, 789, ss="poi", dd="qwe")
    # b(123, 456, 789, dd="qwe")
