import json
from shutil import copyfile

from html处理 import *
from spider import *
from tools import *


class WxGzhSpider:
    def __init__(self, url):
        self.wxset_url = url
        self.album_id = ''
        self.articleurl = []
        self.articlinfolist = []
        self.dir_name = ''
        # self.head = HEAD
        # self.cookie = COOKIE
        self.__get_album_id()
        # self.__n_roll_list = 0

    def __get_album_id(self):
        re_str = r'album_id=(.*?)&'  # 要改成非贪婪加上'?':.*?
        res = re.search(re_str, self.wxset_url)
        if res:
            self.album_id = res.group(1)
        else:
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
        # 判断正倒序 sign=0表示正序 sign=1表示倒序
        sign = 0 if html_tree.xpath(positive_order_xpath) else 1
        # 得到合集关键数据
        data = html_tree.xpath(articleurl_list_xpath)[0]
        first_begin_msgid = data.attrib["data-msgid"]
        self.articleurl.append(data.attrib["data-link"])
        self.get_roll_json(first_begin_msgid)
        if sign:
            self.articleurl.reverse()

    def get_roll_json(self, begin_msgid):
        # print(self.album_id)
        # response = requests.get(url=ROLL_URL.format(begin_msgid=begin_msgid))
        url = ROLL_URL.format(begin_msgid=begin_msgid, album_id=self.album_id)
        # print(url)
        text = get_url_data(url=url)
        # print(text)

        roll_json = json.loads(text)
        # 如果roll_json['base_resp']['ret']为-1表示url错误,返回一个错误码
        if roll_json['base_resp']['ret'] == -1:
            print(f"url错误:{url}")
            return -1
        # 如果有结果
        next_begin_msgid = 0
        if article_list := roll_json["getalbum_resp"].get('article_list', 0):
            # 如果是list的情况
            # print(f"{self.__n_roll_list}有效url:{url}")
            # self.__n_roll_list += 1
            if type(article_list) is list:
                [self.articleurl.append(i["url"]) for i in article_list]
                next_begin_msgid = article_list[-1]['msgid']
            # 如果是dict的情况
            elif type(article_list) is dict:
                self.articleurl.append(article_list['url'])
                next_begin_msgid = article_list['msgid']
        # 没有了结束
        else:
            # print(f"url结束:{url}")
            return 0
        self.get_roll_json(next_begin_msgid)

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
        mkdir(self.dir_name)
        copyfile(edit_css_name, f'{self.dir_name}/{edit_css_name}')
        copyfile(book_css_name, f'{self.dir_name}/{book_css_name}')
        copyfile(vue_js_name, f'{self.dir_name}/{vue_js_name}')
        return

    def test(self):
        self.get_articleurl_list()
        # print(self.articleurl)
        self.init_dir()
        for index, i in enumerate(self.articleurl):
            if index == 3:
                title = write_html(self.dir_name, get_url_data(url=i))
                self.articlinfolist.append({
                    'name': title,
                    'path': f'{title}.html'
                })
                print(f'{index}. {i}:写入完毕')
                # time.sleep(1)
        writ_index_html(self.dir_name, self.articlinfolist)

    def run(self):
        self.get_articleurl_list()
        # print(self.articleurl)
        self.init_dir()
        for index, i in enumerate(self.articleurl):
            title = write_html(self.dir_name, get_url_data(url=i))
            self.articlinfolist.append({
                'name': title,
                'path': f'{title}.html'
            })
            print(f'{index}. {i}:写入完毕')
            # time.sleep(1)
        writ_index_html(self.dir_name, self.articlinfolist)


if __name__ == '__main__':
    url = 'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&action=getalbum&album_id=2554548509648060418&scene=173&from_msgid=2247510881&from_itemidx=1&count=3&nolastread=1#wechat_redirect'
    spider_test = WxGzhSpider(url)
    spider_test.run()
    # spider_test.test()
