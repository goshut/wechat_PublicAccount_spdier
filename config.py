URL = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3NTczMDU2Mg==&action=getalbum&album_id=2206970536067497985&scene=173&from_msgid=2247493173&from_itemidx=1&count=3&nolastread=1#wechat_redirect"
ROLL_URL = "https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&__biz=Mzg3NTczMDU2Mg==&album_id={album_id}&count=20&begin_msgid={begin_msgid}&begin_itemidx=1&uin=&key=&pass_ticket=&wxtoken=&devicetype=&clientversion=&__biz=Mzg3NTczMDU2Mg%3D%3D&appmsg_token=&x5=0&f=json"
HEAD = ""
COOKIE = ""
favicon_name = "favicon.ico"
edit_css_name = 'edit.css'
book_css_name = 'book.css'
vue_js_name = 'vue.global.js'
img_static_dir = 'img'
vue_need_dir_name = "assets"  # vue3依赖文件夹
image_prefix = 'https://mmbiz.qpic.cn/mmbiz_png/'

# html处理相关
DATE_PATH = "/html/body[@id='activity-detail']/div[@id='js_article']/div[@id='js_base_container']/div[@id='page-content']/div[@class='rich_media_area_primary_inner']/div[@id='img-content']"
LAJI_PATH = "//div[@id='js_content']"
TITLE_PATH = "//h1[@id='activity-name']/text()"
image_xpath = '//img'

# spider相关
articleurl_list_xpath = "//li[@class='album__list-item js_album_item js_wx_tap_highlight wx_tap_cell']"
dir_name_xpath = '//div[@id="js_tag_name"]/text()'
positive_order_xpath = '//div[@class="js_positive_order"]/@style'
