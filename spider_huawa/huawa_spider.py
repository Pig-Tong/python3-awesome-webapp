# _*_ coding:utf-8 _*_
import re
from common.img_to_string import img_to_string
from spider_huawa.huawa_area import get_huawa_area
import random
import urllib.request
import xlwt
import os
import gzip
import requests
import time

ip_list = []

ua_list = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
           "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
           "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
           "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
           "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
           "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
           "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
           "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
           "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
           "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
           "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
           ]


# 加载代理ip
def get_ip_list():
    # for i in range(1, 10):
    #     url = 'http://www.xicidaili.com/nn/' + str(i)
    #     headers = {
    #         'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    #                       r' Chrome/70.0.3538.67 Safari/537.36'}
    #     response = urllib.request.Request(url=url, headers=headers)
    #     html = urllib.request.urlopen(response).read().decode('utf-8')
    #     ip_reg = r'<td>(                \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>\s*?<td>(\d*)</td>'
    #     matcher = re.compile(ip_reg)
    #     ip_str = re.findall(matcher, html)
    #
    #     for ip_port in ip_str:
    #         ip_list.append(ip_port[0] + ':' + ip_port[1])
    #         print(ip_port[0] + ':' + ip_port[1])
    with open(os.path.join(os.path.abspath("."), "config", "ip_list.txt"), 'r', encoding='UTF-8', errors='ignore') as f:
        for line in f.readlines():
            ip_list.append(line.strip())
    return ip_list


# 加载页面
def load_page(url):
    print(url)
    user_agent = random.choice(ua_list)
    cookie = "_qddaz=QD.qe65no.gjqtrf.jocwoiln; __cfduid=d6b14c69a3ef3670e10335ae439fdaa521541942382; tencentSig=3793054720; 4047_seccode52f9dc26=055GxTiIdf44GhmdjxCHJo7qafosSfKI2pNd4Vpu4oNj85Jx19g; _qdda=3-1.1; _qddamta_4006780020=3-0; 53kf_1827303_keyword=; PHPSESSID=bb8br5gef4ohelodo7msjkqi07; Hm_lvt_4175f2a72ac6f0c111ec482d34734339=1543421255,1543455179,1543499780,1543500345; Hm_lpvt_4175f2a72ac6f0c111ec482d34734339=1543500345; _qddab=3-hg2kfk.jp2o96dj"
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive", "Cookie": cookie, "Host": "www.huawa.com", "Referer": url,
               "User_Agent": user_agent, "x-requested-with": "XMLHttpRequest"}

    # 随机使用一个代理
    proxy_addr = random.choice(ip_list)
    print("正在使用代理：%s" % proxy_addr)
    # proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    # opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    # urllib.request.install_opener(opener)
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req)
    rsp_headers = res.info()
    html = res.read()
    ret = ""
    if ('Content-Encoding' in rsp_headers and rsp_headers['Content-Encoding'] == 'gzip') or (
            'content-encoding' in rsp_headers and rsp_headers['content-encoding'] == 'gzip'):
        print("is gzip")
        ret = gzip.decompress(html).decode("utf-8")
    else:
        ret = str(html, encoding="utf-8")
    return ret
    # proxies = {
    #     'http': 'http://' + proxy_addr,
    #     'https': 'https://' + proxy_addr,
    # }
    #
    # response = requests.get(url, headers=headers, verify=False)  # 使用requests进行请求时，直接调用requests.get()即可
    # return response.text


# 加载数据
def load_data(province_id, province_name, city_id, city_name, county_id, county_name):
    if os.path.exists(os.path.join(os.path.abspath("."), province_name, city_name,
                                   (province_name + city_name + county_name + '.xls'))):
        return None

    data_list = []
    for i in range(1, 200):
        print("正在收集 %s%s%s 第 %s 页数据" % (province_name, city_name, county_name, str(i)))
        url = 'http://www.huawa.com/store-' + str(province_id) + '-' + str(city_id) + '-' + \
              str(county_id) + '-0-0-0-0-0-' + str(i) + '.html'

        html = load_page(url)
        # 解析数据
        page_list = parse_one_page(html)
        data_list.extend(page_list)
        if len(page_list) < 8:
            break
        time.sleep(2)
    if len(page_list) > 0:
        write_list_to_excel(data_list, province_name, city_name, county_name)


# 解析一个页面
def parse_one_page(html):
    print(html)
    result_list = []
    pattern = re.compile(
        '<span class="diqu">\[(.*?)\].<b><a href="http://www.huawa.com/shop/(.*?)" target="_blank">(.*?)</a>'
        '.*?600;">(.*?)</font>.*?花店电话:<img src="(.*?)".*?花店地址：(.*?)</p>.*?xinyu.*?title="(.*?)"',
        re.S)
    items = re.findall(pattern, html)
    print(items)
    for item in items:
        result = {
            "id": item[1],
            "area": item[0],
            "name": item[2],
            "address": item[5],
            "tel": img_to_string(item[4]),
            "status": item[3],
            "other": item[6],
            "location": get_point_by_id(item[1])
        }
        print(result)
        result_list.append(result)
    return result_list


# 根据id，获取坐标
def get_point_by_id(store_id):
    url = 'http://www.huawa.com/index.php?c=store_list&a=map&store_id=' + str(store_id)
    html = load_page(url)
    pattern = re.compile('"y_axis":"(.*?)","x_axis":"(.*?)"', re.S)
    items = re.findall(pattern, html)
    if len(items):
        return str(items[0][1]) + ',' + str(items[0][0])
    else:
        return ""


# 打印到excel
def write_list_to_excel(data_list, province, city, county):
    province_file = os.path.join(os.path.abspath("."), province)
    if not os.path.exists(province_file):
        os.mkdir(province_file)

    city_file = os.path.join(os.path.abspath("."), province, city)
    if not os.path.exists(city_file):
        os.mkdir(city_file)

    # 将sql作为参数传递调用get_data并将结果赋值给result,(result为一个嵌套元组)
    # 实例化一个Workbook()对象(即excel文件)
    wbk = xlwt.Workbook()
    # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    # 获取当前日期，得到一个datetime对象如：(2016, 8, 9, 23, 12, 23, 424000)
    # today = datetime.today()
    # 将获取到的datetime对象仅取日期如：2016-8-9
    # today_date = datetime.date(today)
    sheet.write(0, 0, "id")
    sheet.write(0, 1, "所在省")
    sheet.write(0, 2, "所在市")
    sheet.write(0, 3, "所在区")
    sheet.write(0, 4, "花店名称")
    sheet.write(0, 5, "花店地址")
    sheet.write(0, 6, "花店电话")
    sheet.write(0, 7, "经纬度")
    sheet.write(0, 8, "状态")
    sheet.write(0, 9, "其他")

    # 遍历result中的没个元素。
    for i in range(len(data_list)):
        # 对result的每个子元素作遍历，
        sheet.write(i + 1, 0, data_list[i]["id"])
        sheet.write(i + 1, 1, province)
        sheet.write(i + 1, 2, city)
        sheet.write(i + 1, 3, county)
        sheet.write(i + 1, 4, data_list[i]["name"])
        sheet.write(i + 1, 5, data_list[i]["address"])
        sheet.write(i + 1, 6, data_list[i]["tel"])
        sheet.write(i + 1, 7, data_list[i]["location"])
        sheet.write(i + 1, 8, data_list[i]["status"])
        sheet.write(i + 1, 9, data_list[i]["other"])

    excel_path = os.path.join(os.path.abspath("."), province, city, (province + city + county + '.xls'))
    wbk.save(excel_path)


if __name__ == "__main__":
    get_ip_list()
    area_list = get_huawa_area()
    for province in area_list[0]:
        province_id = int(province[0])
        province_name = province[1]
        for city in area_list[province_id]:
            city_id = int(city[0])
            city_name = city[1]
            county_array = area_list[city_id]
            if county_array:
                for county in county_array:
                    county_id = int(county[0])
                    county_name = county[1]
                    load_data(province_id, province_name, city_id, city_name, county_id, county_name)
            else:
                load_data(province_id, province_name, city_id, city_name, 0, "")
