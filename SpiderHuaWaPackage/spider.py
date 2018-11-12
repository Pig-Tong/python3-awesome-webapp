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
    url = 'http://www.huawa.com/store/search'
    html = get_one_page(url)
    print(html)

def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
        re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip()
        }

main()
