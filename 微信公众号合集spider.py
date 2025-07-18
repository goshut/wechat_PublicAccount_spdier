import asyncio
import json

# import functools
from shutil import copyfile, copytree

import httpx

from time_code import *
from html处理 import *
from spider import *
from tools import *


class WxGzhSpider:
    file_dir = os.path.dirname(__file__)
    project_dir = file_dir
    templates_dir = f"{project_dir}/templates"

    def __init__(self, _url):
        self.wxset_url = _url
        self.album_id = ""
        self.articleurl = []
        self.articlinfolist = []
        self.dir_name = ""
        # self.head = HEAD
        # self.cookie = COOKIE
        self.__get_album_id()
        # self.__n_roll_list = 0
        # 为了方便git忽略..统一将输出文件夹放在output
        self.output_dir = f"{WxGzhSpider.project_dir}/output"
        mkdir(self.output_dir)
        # 异步请求网络
        self.client = AySpider()

    # @functools.cached_property
    @property
    def save_dir(self):
        return f"{self.output_dir}/{self.dir_name}"

    def __get_album_id(self):
        re_str = r"album_id=([\d]+)"  # 要改成非贪婪加上'?':.*?
        res = re.search(re_str, self.wxset_url)
        if res:
            self.album_id = res.group(1)
        else:
            print("__get_album_id:退出")
            exit(-1)

    def get_articleurl_list(self):
        # 第一次构建
        # response = requests.get(url=self.wxset_url)
        # text = response.text
        html_tree = get_url_html_tree(url=self.wxset_url)
        # 得到文件夹名
        # print(etree.tounicode(html_tree, method='html'))
        self.dir_name = html_tree.xpath(dir_name_xpath)[0]
        self.dir_name = clean_str(self.dir_name)
        # self.dir_name = f"{self.output_dir}/{clean_str(self.dir_name)}"
        # 判断正倒序 sign=0表示正序 sign=1表示倒序
        sign = 0 if html_tree.xpath(positive_order_xpath) else 1
        # 得到合集关键数据
        articleurl_list = html_tree.xpath(articleurl_list_xpath)
        i = {}
        for i in articleurl_list:
            self.articleurl.append(i.attrib["data-link"])
        else:
            first_begin_msgid = i.get("data-msgid", None)
            itemidx = i.get("data-itemidx", 1)
        # data = html_tree.xpath(articleurl_list_xpath)[0]
        # first_begin_msgid = data.attrib["data-msgid"]
        # self.articleurl.append(data.attrib["data-link"])

        self.get_roll_json(first_begin_msgid, itemidx)
        if sign:
            self.articleurl.reverse()

    def get_roll_json(self, begin_msgid, itemidx=1):
        # print(self.album_id)
        # response = requests.get(url=ROLL_URL.format(begin_msgid=begin_msgid))
        url = ROLL_URL.format(begin_msgid=begin_msgid, album_id=self.album_id, itemidx=itemidx)
        # print(url)
        text = get_url_data(url=url)
        # print(text)

        roll_json = json.loads(text)
        # 如果roll_json['base_resp']['ret']为-1表示url错误,返回一个错误码
        if roll_json["base_resp"]["ret"] == -1:
            print(f"url错误:{url}")
            return -1
        # 如果有结果
        next_begin_msgid = 0
        if article_list := roll_json["getalbum_resp"].get("article_list", 0):
            # 如果是list的情况
            # print(f"{self.__n_roll_list}有效url:{url}")
            # self.__n_roll_list += 1
            if type(article_list) is list:
                [self.articleurl.append(i["url"]) for i in article_list]
                next_begin_msgid = article_list[-1]["msgid"]
                itemidx = article_list[-1]["itemidx"]
            # 如果是dict的情况
            elif type(article_list) is dict:
                self.articleurl.append(article_list["url"])
                next_begin_msgid = article_list["msgid"]
                itemidx = article_list["itemidx"]
        # 没有了结束
        else:
            # print(f"url结束:{url}")
            return 0
        self.get_roll_json(next_begin_msgid, itemidx)

    # @staticmethod
    # def get_url_data(url):
    #     return requests.get(url).text
    #
    # @classmethod
    # def get_url_html_tree(cls, url):
    #     text = cls.get_url_data(url)
    #     html_tree = etree.HTML(text)
    #     return html_tree

    def init_dir(self):
        mkdir(self.save_dir)
        copyfile(
            f"{WxGzhSpider.templates_dir}/{edit_css_name}",
            f"{self.save_dir}/{edit_css_name}",
        )
        # copyfile(book_css_name, f'{self.save_dir}/{book_css_name}')
        copytree(
            f"{WxGzhSpider.templates_dir}/{vue_need_dir_name}",
            f"{self.save_dir}/{vue_need_dir_name}",
            dirs_exist_ok=True,
        )
        copyfile(
            f"{WxGzhSpider.templates_dir}/{favicon_name}",
            f"{self.save_dir}/{favicon_name}",
        )
        return

    def test(self):
        self.get_articleurl_list()
        # print(self.articleurl)
        self.init_dir()
        for index, i in enumerate(self.articleurl):
            if index == 3:
                title = write_html(self.save_dir, get_url_data(url=i))
                # self.articlinfolist.append({
                #     'name': title,
                #     'path': f'{title}.html'
                # })
                self.articlinfolist.append(title)
                print(f"{index}. {i}:写入完毕")
                # time.sleep(1)
        writ_index_html(self.save_dir, self.articlinfolist)

    def run(self):
        self.get_articleurl_list()
        # print(self.articleurl)
        self.init_dir()
        for index, i in enumerate(self.articleurl):
            title = write_html(self.save_dir, get_url_data(url=i))
            # self.articlinfolist.append({
            #     'name': title,
            #     'path': f'{title}.html'
            # })
            self.articlinfolist.append(title)
            print(f"{index}. {i}:写入完毕")
            # time.sleep(1)
        writ_index_html(self.save_dir, self.articlinfolist)

    async def ay_deal_articleurl_data(self, _url, index):
        print(f"{index}. {_url} :正在处理")
        title, article = "no_title", "no_article"
        tries = 5
        deal_ok_sign = True
        res_tulble = None
        response = None
        i = 0
        for i in range(tries):
            response = await self.client.get(url=_url)
            # response = httpx.get(url)
            # print("\n" * 3)
            # print(response.headers)
            # print(response.http_version)  # HTTP/2
            res_tulble = await ay_get_article(response.text, self.save_dir)
            if res_tulble:
                title, article = res_tulble
                break
            else:
                print(response.status_code)
                print(f"获取{_url}失败,第{i + 1}次尝试重试.")
                # 这种情况是异步获取速度太快,微信服务器反应不过来,就用一个垃圾页面来糊弄...当然也有可能是防御措施..但这未免也太弱了...
                # 5次失败后...就创建一个空页面以后解决
                if i < tries:
                    await asyncio.sleep(0.2)
        else:
            if not res_tulble:
                deal_ok_sign = False

        # 输出处理结果信息
        if not deal_ok_sign:
            if response: print(response.text)
            print(f"{index}. {_url} :处理失败")
        elif i > 0:
            print(f"{index}. 在第{i + 1}次尝试成功,处理完成")
        else:
            print(f"{index}. 处理完成")
        return await ay_write_html(self.save_dir, title, article)

    async def async_run(self):
        self.get_articleurl_list()
        # print(self.articleurl)
        self.init_dir()
        async with self.client:
            self.articlinfolist = await asyncio.gather(
                *[
                    self.ay_deal_articleurl_data(i, index)
                    for index, i in enumerate(self.articleurl)
                ]
            )
            writ_index_html(self.save_dir, self.articlinfolist)
            all_tasks = asyncio.all_tasks()
            all_tasks.discard(asyncio.current_task())
            if all_tasks:
                await asyncio.wait(all_tasks)


if __name__ == "__main__":
    with CodeTimer():
        # python web 开发
        # url = 'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&action=getalbum&album_id=2815412073764454403&subscene=159&subscene=&scenenote=https%3A%2F%2Fmp.weixin.qq.com%2Fs%2FHQ0mbeb6bTik3cwg6skyLg&nolastread=1#wechat_redirect'
        # python奇奇怪怪
        # url = 'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&action=getalbum&album_id=2735429956649844737&subscene=159&subscene=&scenenote=https%3A%2F%2Fmp.weixin.qq.com%2Fs%2FD1_WLV3odUwA12_E3PssPg&nolastread=1#wechat_redirect'
        # 网络协议与操作系统
        # url = 'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&action=getalbum&album_id=2411327902559666177&scene=21#wechat_redirect'
        # redis 这个网址直接-1滚出,连报错都没有!!!!!
        # url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&action=getalbum&album_id=2554548509648060418#wechat_redirect"
        # 大数据组件  ...只有一个页面,列表url只有1???
        # url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&action=getalbum&album_id=2608550406499041280&scene=21#wechat_redirect"
        # python的背后
        # url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&action=getalbum&album_id=2516744157244129282#wechat_redirect"
        # cython
        # url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&action=getalbum&album_id=2513963764346486784#wechat_redirect"
        # rust
        # url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&action=getalbum&album_id=2583473431749296129&scene=21#wechat_redirect"
        # mysql
        url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&action=getalbum&album_id=2432737848694046721#wechat_redirect"
        # python实用技巧 有40多个!!
        url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&action=getalbum&album_id=2413802396947742721#wechat_redirect"
        url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAwNzk2OTQ4MQ==&action=getalbum&album_id=3204441673276194816&subscene=159&subscene=&scenenote=https%3A%2F%2Fmp.weixin.qq.com%2Fs%2FHwxYZqz6MqANViNwSylvJw&nolastread=1#wechat_redirect"
        spider_test = WxGzhSpider(url)
        # spider_test.run()
        asyncio.run(spider_test.async_run())
        # spider_test.test()
