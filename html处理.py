import asyncio
import os.path

from jinja2 import Environment, FileSystemLoader

from config import *
from spider import *
from tools import *

file_dir = os.path.dirname(__file__)
project_dir = file_dir
env = Environment(loader=FileSystemLoader(f"{project_dir}/templates"))
template = env.get_template("template.html")
index_template = env.get_template("vue_重构_index_template.html")
client = AySpider()  # 具有全局唯一性


# ay_tasks = []


def get_article(html_date, save_dir_path):
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
    article_tree = img_deal(article_tree, save_dir_path)
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


def write_html(save_dir_path, html_date):
    # base_dir_name = os.path.basename(save_dir_path)
    title, article = get_article(html_date, save_dir_path)
    data = merge_template(title, article)
    same_name[title] = same_name.get(title, 0) + 1
    if same_name[title] > 1:  # 如果有相同名字的html文件了,加上后缀
        title = f"{title}{same_name[title]}"
    with open(f"{save_dir_path}/{title}.html", "w", encoding="utf-8") as f:
        f.write(data)
    return title


def img_deal(tree_, save_dir_path):
    img_dir_path = f"{save_dir_path}/{img_static_dir}"
    mkdir(img_dir_path)
    image_list = tree_.xpath(image_xpath)
    for index, i in enumerate(image_list):
        if image_url := i.attrib.get("data-src"):
            img_name = get_image_name(image_url)
            file_name = f"{img_dir_path}/{img_name}.png"
            # 判断imag是否存在
            if not os.path.exists(file_name):
                writ_get_data(url=image_url, file_name=file_name)
            file_name_of_html = f"{img_static_dir}/{img_name}.png"
            i.attrib["src"] = file_name_of_html
            del i.attrib["data-src"]
    return tree_


def get_image_name(wximg_url):
    img_name = re.sub(image_prefix, "", wximg_url)
    img_name = clean_str(img_name)
    return img_name


def writ_get_data(url, file_name):
    with open(file_name, "wb") as f:
        f.write(requests.get(url=url).content)


def writ_index_html(save_dir_path, article_info_list):
    book_name = os.path.basename(save_dir_path)
    new_html = index_template.render(
        title=book_name,
        # book_name=book_name,
        article_info_list=article_info_list,
    )
    with open(f"{save_dir_path}/index.html", "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"{book_name} index.html写入完毕!")


# 异步重构版本
# 真恶心啊,异步是有传染性吗?整个调用链全异步化了
# 修改原始的链式调用为分步调用
####################
####################
# 先取得文章标题和imageurl信息
# 创建异步imageurl数据获取任务
# 保存文章标题html


async def ay_write_html(save_dir_path, title, article):
    # title, article = await ay_get_article(html_date, save_dir_path)
    data = merge_template(title, article)
    same_name[title] = same_name.get(title, 0) + 1
    if same_name[title] > 1:  # 如果有相同名字的html文件了,加上后缀
        title = f"{title}{same_name[title]}"
    with open(f"{save_dir_path}/{title}.html", "w", encoding="utf-8") as f:
        f.write(data)
    return title


async def ay_get_article(html_date, save_dir_path):
    """
    :param html_date: 一个html文档utf-8编码
    :return:标题和微信公众号文章有用的部分..
    """

    html_tree = etree.HTML(html_date)
    try:
        article_tree = html_tree.xpath(DATE_PATH)[0]
        laji_tree = article_tree.xpath(LAJI_PATH)[0]
    except Exception as e:
        # print(html_date)
        print(e, end="\n**********************\n")
        # return "no_title", "no_article"
        return None
    del laji_tree.attrib["style"]  # 垃圾属性会隐藏....
    title = article_tree.xpath(TITLE_PATH)[0].strip()
    title = clean_str(title)
    # 先进行图片处理
    article_tree = await ay_img_deal(article_tree, save_dir_path)
    article = etree.tounicode(article_tree, method="html")
    return title, article


async def ay_img_deal(tree_, save_dir_path):
    global ay_tasks
    img_dir_path = f"{save_dir_path}/{img_static_dir}"
    mkdir(img_dir_path)
    image_list = tree_.xpath(image_xpath)
    for index, i in enumerate(image_list):
        if image_url := i.attrib.get("data-src"):
            img_name = get_image_name(image_url)
            file_name = f"{img_dir_path}/{img_name}.png"
            # 判断imag是否存在
            if not os.path.exists(file_name):
                # writ_get_data(url=image_url, file_name=file_name)
                # ay_tasks.append(asyncio.create_task(ay_writ_get_data(url=image_url, file_name=file_name)))
                asyncio.create_task(
                    ay_writ_get_data(url=image_url, file_name=file_name)
                )
            file_name_of_html = f"{img_static_dir}/{img_name}.png"
            i.attrib["src"] = file_name_of_html
            del i.attrib["data-src"]
    # await asyncio.gather(*ay_tasks)
    return tree_


async def ay_writ_get_data(url, file_name):
    response = await client.get(url=url)
    with open(file_name, "wb") as f:
        f.write(response.content)


if __name__ == "__main__":
    get_image_name(
        "https://mmbiz.qpic.cn/mmbiz_png/HlNkQjetfwiaeG2eibibS4RBQY8AFicia9q36jicvERnwdOiatCCicr8H3m5do4ZANHLuqF8yiawknQEaR6LFmL7e97iazfA/640?wx_fmt=png"
    )
