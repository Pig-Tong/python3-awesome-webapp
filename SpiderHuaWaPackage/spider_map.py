# _*_ coding:utf-8 _*_
import json
import re
import time
import urllib.request
import xlwt
from datetime import datetime
import random
import os


# 加载代理ip
def get_ip_list():
    ip_list = []
    for i in range(1, 10):
        url = 'http://www.xicidaili.com/nn/' + str(i)
        headers = {
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          r' Chrome/70.0.3538.67 Safari/537.36'}
        response = urllib.request.Request(url=url, headers=headers)
        html = urllib.request.urlopen(response).read().decode('utf-8')
        ip_reg = r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>\s*?<td>(\d*)</td>'
        matcher = re.compile(ip_reg)
        ip_str = re.findall(matcher, html)

        for ip_port in ip_str:
            ip_list.append(ip_port[0] + ':' + ip_port[1])
            print(ip_port[0] + ':' + ip_port[1])
    return ip_list


def main():
    ip_list = get_ip_list()
    area_str = ""
    with open(r'C:\Users\pig\Desktop\area.json', 'r', encoding='UTF-8', errors='ignore') as f:
        for line in f.readlines():
            area_str += line.strip()
    area_json = json.loads(area_str)

    # 省会
    for province in [x for x in area_json if x["ParentId"] == 0]:
        province_id = province["AreaId"]
        province_name = province["Name"]
        # 循环城市
        for city in [x for x in area_json if x["ParentId"] == province_id]:
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

    # load_data(510100, "成都", "成都", ip_list)


# 处理数据
def load_data(area_id, province, city, county, ip_list):
    temp = []
    for i in range(1, 100):
        print("正在收集 %s%s%s 第 %s 页数据" % (province, city, county, str(i)))
        url = 'https://www.amap.com/service/poiInfo?query_type=TQUERY&pagesize=20&pagenum=' + str(
            i) + '&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=12&city=' + str(
            area_id) + '&keywords=%E8%8A%B1%E5%BA%97'
        html = str(load_page(url, ip_list), encoding="utf8")
        print(html)
        # 转json
        json_data = json.loads(html)
        # list
        if "poi_list" in json_data["data"].keys():
            list = json_data["data"]["poi_list"]
            for elem in list:
                temp.append(elem)
        else:
            break
        time.sleep(2)

    write_list_to_excel(temp, province, city, county)


# 加载页面
def load_page(url, ip_list):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/70.0.3538.77 Safari/537.36"
    cookie = "UM_distinctid=16712ac667d18b-0c2f90b5be927-b79183d-100200-16712ac667fa8b; cna=I13fEQPsO0ICAd9XIcqaeqnA; _uab_collina=154220655304732961312653; key=bfe31f4e0fb231d29e1d3ce951e2c780; CNZZDATA1255626299=1772599595-1542204043-https%253A%252F%252Fwww.baidu.com%252F%7C1542935321; x5sec=7b22617365727665723b32223a2230346362343166623937366232326463393538383137316662316364353863624350584333643846454b7a543259726d754b715962513d3d227d;"
    headers = {"User_Agent": user_agent, "cookie": cookie, "Host": "www.amap.com",
               "amapuuid": "234cfd23-466d-473a-8438-ea5a53333e6e"}

    # 随机使用一个代理
    proxy_addr = random.choice(ip_list)
    print("正在使用代理：%s" % proxy_addr)
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req)
    html = res.read()
    return html


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
    sheet.write(0, 1, "所在城市")
    sheet.write(0, 2, "花店名称")
    sheet.write(0, 3, "花店电话")
    sheet.write(0, 4, "花店地址")
    sheet.write(0, 5, "经度")
    sheet.write(0, 6, "纬度")
    sheet.write(0, 7, "花店名称")

    # 遍历result中的没个元素。
    for i in range(len(data_list)):
        # 对result的每个子元素作遍历，
        for j in range(len(data_list[i])):
            # 将每一行的每个元素按行号i,列号j,写入到excel中。
            sheet.write(i + 1, 0, data_list[i]["id"])
            sheet.write(i + 1, 1, data_list[i]["cityname"])
            sheet.write(i + 1, 2, data_list[i]["name"])
            sheet.write(i + 1, 3, data_list[i]["tel"])
            sheet.write(i + 1, 4, data_list[i]["address"])
            sheet.write(i + 1, 5, data_list[i]["longitude"])
            sheet.write(i + 1, 6, data_list[i]["latitude"])
            if "disp_name" in data_list[i].keys():
                sheet.write(i + 1, 7, data_list[i]["disp_name"])

    # 以传递的name+当前日期作为excel名称保存。
    excel_path = os.path.join(os.path.abspath("."), province, city, (province + city + county + '.xls'))
    wbk.save(excel_path)
    with open('C:\\Users\\pig\Desktop\新建文本文档.txt', 'a', encoding='UTF-8', errors='ignore') as f:
        f.writelines(str(len(data_list))+"\n")


main()
