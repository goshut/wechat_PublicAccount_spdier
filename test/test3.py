import os

from jinja2 import PackageLoader, Environment

env = Environment(loader=PackageLoader("微信_公众号", "templates"))
template = env.get_template("index_template.html")

title = "标题"
book_name = "合集名"
article_info_list = []


# article_info = {
#     'filename': '文件名',
#     'filepath_of_html': '文件相对位置',
# }
# for i in range(20):
#     article_info_list.append(f'{i}test_name')
def get_article_info_list(path):
    return os.listdir(path)


offset_path = '../CPython源码探秘'
[article_info_list.append(f'{offset_path}/{i}') for i in get_article_info_list(offset_path)]
# article_info_list += get_article_info_list(offset_path)
new_html = template.render(title=title,
                           book_name=book_name,
                           article_info_list=article_info_list)
with open("test33.html", 'w', encoding='utf-8') as f:
    f.write(new_html)

# response = requests.get("https://unpkg.com/vue@3/dist/vue.global.js")
# with open("../vue.global.js", 'wb') as f:
#     f.write(response.content)
