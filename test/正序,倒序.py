from lxml import etree

with open('raw_cpython.html', 'r', encoding='utf8') as f:
    html = etree.HTML(f.read())
xpath = '//div[@class="js_positive_order"]/@style'
xpath2 = '//div[@class="js_negative_order"]/@style'

xpath_list = html.xpath(xpath)
if xpath_list:
    print(xpath_list)
xpath_list = html.xpath(xpath2)
if xpath_list:
    print(xpath_list)

a = [1, 2, 3, 4]
a.reverse()
print(a)
