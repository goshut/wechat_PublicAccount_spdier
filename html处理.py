import os.path

from jinja2 import Environment, PackageLoader

from config import *
from spider import *
from tools import *

env = Environment(loader=PackageLoader("微信_公众号", "templates"))
template = env.get_template("template.html")
index_template = env.get_template("index_template.html")


def get_article(html_date, dir_name):
    """
    :param html_date: 一个html文档utf-8编码
    :return:标题和微信公众号文章有用的部分..
    """
    html_tree = etree.HTML(html_date)
    article_tree = html_tree.xpath(DATE_PATH)[0]
    laji_tree = article_tree.xpath(LAJI_PATH)[0]
    del laji_tree.attrib["style"]  # 垃圾属性会隐藏....
    title = article_tree.xpath(TITLE_PATH)[0].strip()
    title = clean_str(title)
    # 先进行图片处理
    article_tree = img_deal(article_tree, dir_name)
    article = etree.tounicode(article_tree, method="html")
    return title, article


def merge_template(title, article):
    """
    将内容合并模板
    :param title: 标题
    :param article: 文章
    :return:字符串
    """
    return template.render(title=title, article=article)


same_name = {}


def write_html(dir_name, html_date):
    title, article = get_article(html_date, dir_name)
    data = merge_template(title, article)
    same_name[title] = same_name.get(title, 0) + 1
    if same_name[title] > 1:  # 如果有相同名字的html文件了,加上后缀
        title = f'{title}{same_name[title]}'
    with open(f'{dir_name}/{title}.html', 'w', encoding="utf-8") as f:
        f.write(data)
    return title


def img_deal(tree_, dir_name):
    img_dir_path = f'{dir_name}/{img_static_dir}'
    mkdir(img_dir_path)
    image_list = tree_.xpath(image_xpath)
    for index, i in enumerate(image_list):
        if image_url := i.attrib.get('data-src'):
            img_name = get_image_name(image_url)
            file_name = f'{img_dir_path}/{img_name}.png'
            # 判断imag是否存在
            if not os.path.exists(file_name):
                writ_get_data(url=image_url, file_name=file_name)
            file_name_of_html = f'{img_static_dir}/{img_name}.png'
            i.attrib['src'] = file_name_of_html
            del i.attrib['data-src']
    return tree_


def get_image_name(wximg_url):
    img_name = re.sub(image_prefix, '', wximg_url)
    img_name = clean_str(img_name)
    return img_name


def writ_get_data(url, file_name):
    with open(file_name, 'wb') as f:
        f.write(requests.get(url=url).content)


def writ_index_html(book_name, article_info_list):
    new_html = index_template.render(title=book_name,
                                     book_name=book_name,
                                     article_info_list=article_info_list)
    with open(f'{book_name}/index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"{book_name} index.html写入完毕!")


if __name__ == '__main__':
    get_image_name(
        'https://mmbiz.qpic.cn/mmbiz_png/HlNkQjetfwiaeG2eibibS4RBQY8AFicia9q36jicvERnwdOiatCCicr8H3m5do4ZANHLuqF8yiawknQEaR6LFmL7e97iazfA/640?wx_fmt=png')
