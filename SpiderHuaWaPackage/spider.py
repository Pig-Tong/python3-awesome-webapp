# _*_ coding:utf-8 _*_
import json
import requests
from requests.exceptions import RequestException
import re
import time


def get_one_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def main():

    url = 'http://www.huawa.com/store-24-382-2465-0-0-0-0-0-2.html'
    html = get_one_page(url)
    print(parse_one_page(html))


def parse_one_page(html):
    pattern = re.compile(
        '<span class="diqu">\[(.*?)\].<b><a href="http://www.huawa.com/shop/(.*?)" target="_blank">(.*?)</a>'
        '.*?600;">(.*?)</font>.*?花店地址：(.*?)</p>.*?xinyu.*?title="(.*?)"',
        re.S)
    items = re.findall(pattern, html)
    print(items)
    for item in items:
        print(item)
        # yield {
        #     'area': item[19:],
        #     # 'image': item[1],
        #     # 'title': item[2].strip(),
        #     # 'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
        #     # 'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
        #     # 'score': item[5].strip() + item[6].strip()
        # }


main()
