# _*_ coding:utf-8 _*_
import json
import re
import time
import urllib.request
import xlwt
from datetime import datetime
import random
import os
import gzip


# 加载代理ip
def get_ip_list():
    ip_list = []
    # for i in range(1, 2):
    #     url = 'http://www.xicidaili.com/nn/' + str(i)
    #     headers = {
    #         'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    #                       r' Chrome/70.0.3538.67 Safari/537.36'}
    #     response = urllib.request.Request(url=url, headers=headers)
    #     html = urllib.request.urlopen(response).read().decode('utf-8')
    #     ip_reg = r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>\s*?<td>(\d*)</td>'
    #     matcher = re.compile(ip_reg)
    #     ip_str = re.findall(matcher, html)
    #
    #     for ip_port in ip_str:
    #         ip_list.append(ip_port[0] + ':' + ip_port[1])
    #         print(ip_port[0] + ':' + ip_port[1])
    with open(r'C:\Users\zhut\Desktop\ip_list.txt', 'r', encoding='UTF-8', errors='ignore') as f:
        for line in f.readlines():
            ip_list.append(line.strip())
    return ip_list


def main():
    ip_list = get_ip_list()
    area_str = ""
    with open(r'C:\Users\zhut\Desktop\area.json', 'r', encoding='UTF-8', errors='ignore') as f:
        for line in f.readlines():
            area_str += line.strip()
    area_json = json.loads(area_str)

    # 省会
    for province in [x for x in area_json if x["ParentId"] == 0]:
        province_id = province["AreaId"]
        province_name = province["Name"]
        province_list = [x for x in area_json if x["ParentId"] == province_id]
        if province_list:
            # 循环城市
            for city in province_list:
                city_name = city["Name"]
                city_id = city["AreaId"]
                county_list = [x for x in area_json if x["ParentId"] == city_id]
                if county_list:
                    for county in county_list:
                        county_name = county["Name"]
                        county_id = county["AreaId"]
                        file_path = os.path.join(os.path.abspath("."), province_name, city_name,
                                                 (province_name + city_name + county_name + '.xls'))
                        # 判断文件是否存在
                        if not os.path.exists(file_path):
                            load_data(county_id, province_name, city_name, county_name, ip_list)

                else:
                    file_path = os.path.join(os.path.abspath("."), province_name, (province_name + city_name + '.xls'))
                    # 判断文件是否存在
                    if not os.path.exists(file_path):
                        load_data(city_id, province_name, "", city_name, ip_list)
        else:
            file_path = os.path.join(os.path.abspath("."), province_name, (province_name + '.xls'))
            # 判断文件是否存在
            if not os.path.exists(file_path):
                load_data(province_id, province_name, "", province_name, ip_list)

    # load_data(510100, "成都", "成都", ip_list)


# 处理数据
def load_data(area_id, province, city, county, ip_list):
    temp = []
    for i in range(1, 100):
        print("正在收集 %s%s%s 第 %s 页数据" % (province, city, county, str(i)))
        url = 'https://restapi.amap.com/v3/place/text?keywords=%E8%8A%B1%E5%BA%97&key=80b12f14c0f7435ad11ace33273b1b06&output=json' \
              '&extensions=base&citylimit=true&offset=20&page=' + str(i) + '&city=' + str(area_id)
        html = load_page(url, ip_list)
        print(html)
        # 转json
        json_data = json.loads(html)
        # list
        print(len(json_data["pois"]))
        if len(json_data["pois"]):
            for elem in json_data["pois"]:
                temp.append(elem)
        else:
            break
        time.sleep(2)

    write_list_to_excel(temp, province, city, county)


# 加载页面
def load_page(url, ip_list):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/70.0.3538.77 Safari/537.36"
    cookie = "UM_distinctid=16711c5ccb7d60-02412942692cbd-b79193d-1fa400-16711c5ccb8918; cna=sMDqExMDnCcCAW6480fQ+W4J; _uab_collina=154219143645961913353431; key=bfe31f4e0fb231d29e1d3ce951e2c780; CNZZDATA1255626299=2035170135-1542186042-https%253A%252F%252Fwww.baidu.com%252F%7C1542938615; x5sec=7b22617365727665723b32223a223336316137316439373938366233353030323263323564393831643937343064434b4f7433743846454a7239324b6a52352b373058773d3d227d; "
    headers = {"User_Agent": user_agent, "cookie": cookie, "Host": "restapi.amap.com",
               'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br',
               'clientType': 'web'}

    # 随机使用一个代理
    proxy_addr = random.choice(ip_list)
    print("正在使用代理：%s" % proxy_addr)
    print(url)
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req)
    rspheaders = res.info()
    html = res.read()
    ret = ""
    print(html)
    if ('Content-Encoding' in rspheaders and rspheaders['Content-Encoding'] == 'gzip') or (
            'content-encoding' in rspheaders and rspheaders['content-encoding'] == 'gzip'):
        ret = gzip.decompress(html).decode("utf-8")
    else:
        ret = str(html, encoding="utf-8")

    return ret


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
    today = datetime.today()
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

    # 遍历result中的没个元素。
    for i in range(len(data_list)):
        # 对result的每个子元素作遍历，
        sheet.write(i + 1, 0, data_list[i]["id"])
        sheet.write(i + 1, 1, data_list[i]["pname"])
        sheet.write(i + 1, 2, data_list[i]["cityname"])
        sheet.write(i + 1, 3, data_list[i]["adname"])
        sheet.write(i + 1, 4, data_list[i]["name"])
        sheet.write(i + 1, 5, data_list[i]["address"])
        sheet.write(i + 1, 6, data_list[i]["tel"])
        sheet.write(i + 1, 7, data_list[i]["location"])

    excel_path = os.path.join(os.path.abspath("."), province, city, (province + city + county + '.xls'))
    wbk.save(excel_path)
    with open('C:\\Users\\zhut\Desktop\新建文本文档.txt', 'a', encoding='UTF-8', errors='ignore') as f:
        f.writelines(str(len(data_list)) + "\n")


main()
