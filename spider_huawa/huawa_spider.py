# _*_ coding:utf-8 _*_
import re
from common.img_to_string import img_to_string
from spider_huawa.huawa_area import get_huawa_area
import random
import urllib.request
import xlwt
import os
import gzip

ip_list = []


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
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    cookie = "_qddaz=QD.qe65no.gjqtrf.jocwoiln; __cfduid=d6b14c69a3ef3670e10335ae439fdaa521541942382; " \
             "tencentSig=3793054720; 4047_seccode52f9dc26=055GxTiIdf44GhmdjxCHJo7qafosSfKI2pNd4Vpu4oNj85Jx19g; " \
             "PHPSESSID=mkcc4lbav519pdiqfbikuj4rm3; 53kf_1827303_keyword=; " \
             "Hm_lvt_4175f2a72ac6f0c111ec482d34734339=1543075412,1543075826,1543332343,1543416221; " \
             "Hm_lpvt_4175f2a72ac6f0c111ec482d34734339=1543416221; _qdda=3-1.1; _qddab=3-pedj3t.jp1a62t4; _" \
             "qddamta_4006780020=3-0"

    headers = {"User_Agent": user_agent, "Cookie": cookie, "Host": "www.huawa.com", 'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate'}

    # 随机使用一个代理
    proxy_addr = random.choice(ip_list)
    print("正在使用代理：%s" % proxy_addr)
    print(url)
    # proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    # opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    # urllib.request.install_opener(opener)
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req)
    rsp_headers = res.info()
    html = res.read()
    ret = ""
    print(html)
    if ('Content-Encoding' in rsp_headers and rsp_headers['Content-Encoding'] == 'gzip') or (
            'content-encoding' in rsp_headers and rsp_headers['content-encoding'] == 'gzip'):
        print("is gzip")
        ret = gzip.decompress(html).decode("utf-8")
    else:
        ret = str(html, encoding="utf-8")
    print(ret)
    return ret


# 加载数据
def load_data(province_id, province_name, city_id, city_name, county_id, county_name):
    data_list = []
    for i in range(1, 200):
        print("正在收集 %s%s%s 第 %s 页数据" % (province_name, city_name, county_name, str(i)))
        url = 'http://www.huawa.com/store-' + str(province_id) + '-' + str(city_id) + '-' + \
              str(county_id) + '-0-0-0-0-0-' + str(i) + '.html'
        html = load_page(url)
        print(html)
        # 解析数据
        page_list = parse_one_page(html)
        if len(page_list):
            data_list.extend(page_list)
        else:
            break
    write_list_to_excel(data_list, province_name, city_name, county_name)


# 解析一个页面
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
    return str(items[0][1]) + ',' + str(items[0][0])


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
