# _*_ coding:utf-8 _*_
import requests
import re
from common.img_to_string import img_to_string


def get_one_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def main():
    # area_list = get_huawa_area()
    # for province in area_list[0]:
    #     province_id = int(province[0])
    #     province_name = province[1]
    #     for city in area_list[province_id]:
    #         city_id = int(city[0])
    #         city_name = city[1]
    #         county_array = area_list[city_id]
    #         if county_array:
    #             for county in county_array:
    #                 county_id = int(county[0])
    #                 county_name = county[1]
    #                 print(province_name, city_name, county_name)
    #         else:
    #             print(province_name, city_name)
    url = 'http://www.huawa.com/store-24-382-2465-0-0-0-0-0-1.html'
    html = get_one_page(url)
    parse_one_page(html)
    url = 'http://www.huawa.com/index.php?c=store_list&a=map&store_id=422422'
    html = get_one_page(url)
    parse_one_point(html)


def parse_one_page(html):
    result_list = []
    pattern = re.compile(
        '<span class="diqu">\[(.*?)\].<b><a href="http://www.huawa.com/shop/(.*?)" target="_blank">(.*?)</a>'
        '.*?600;">(.*?)</font>.*?花店电话:<img src="(.*?)".*?花店地址：(.*?)</p>.*?xinyu.*?title="(.*?)"',
        re.S)
    items = re.findall(pattern, html)
    for item in items:
        result = {
            "id": item[1],
            "area": item[0],
            "name": item[2],
            "address": item[5],
            "phone": img_to_string(item[4]),
            "status": item[3],
            "other": item[6]
        }
        print(result)
        result_list.append(result)
    return result_list


# 解析坐标
def parse_one_point(html):
    pattern = re.compile(
        '"y_axis":"(.*?)","x_axis":"(.*?)"',
        re.S)
    items = re.findall(pattern, html)
    print(items)
    for item in items:
        print(item[0])
        print(item[1])


main()
