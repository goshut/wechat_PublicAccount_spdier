import requests
from lxml import etree


def get_url_data(url):
    return requests.get(url).text


def get_url_html_tree(url):
    text = get_url_data(url)
    html_tree = etree.HTML(text)
    return html_tree

