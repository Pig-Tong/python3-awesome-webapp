# _*_ coding:utf-8 _*_
import json
import requests
from requests.exceptions import RequestException
import re
import time
import urllib.request
import xlwt
from datetime import datetime
import random
import os

# 代理池
proxy_list = [
    {"http": "114.82.109.134:8118"},
    {"http": "124.88.67.81:80"},
    {"http": "121.193.143.249:80"}
]


# 加载页面
def load_page(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    cookie = "guid=56db-07ca-4e87-f04a; UM_distinctid=16712ac667d18b-0c2f90b5be927-b79183d-100200-16712ac667fa8b; cna=I13fEQPsO0ICAd9XIcqaeqnA; _uab_collina=154220655304732961312653; key=bfe31f4e0fb231d29e1d3ce951e2c780; CNZZDATA1255626299=1772599595-1542204043-https%253A%252F%252Fwww.baidu.com%252F%7C1542290506; x5sec=7b22617365727665723b32223a2264333636356261356336316364376436373938363738633336346239353630374350437374743846454d47696876666939496a4442773d3d227d; isg=BA8PDxgFiOt7zYwWJRSsf1rWnqPZnGMzzISM2SEP2n448AXyegSOpiym9mBriD"

    headers = {"User_Agent": user_agent, "Cookie": cookie, "amapuuid": "234cfd23-466d-473a-8438-ea5a53333e6e",
               "Host": "www.amap.com", "Referer": "https://www.amap.com/"}
    # 随机使用一个代理
    proxy_addr = random.choice(proxy_list)
    print("正在使用代理：%s" % proxy_addr)
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req)
    html = res.read()
    return html


def main():
    # areaStr = ""
    # with open(r'C:\\Users\\pig\Desktop\area.json', 'r', encoding='UTF-8', errors='ignore') as f:
    #     for line in f.readlines():
    #         areaStr += line.strip()
    # areaJson = json.loads(areaStr)
    # for area in areaJson:
    #     if area["ParentId"] == 510000:
    #         print(area["AreaId"], area["Name"])

    temp = []
    for i in range(1, 35):
        print("正在收集第 " + str(i) + " 页数据")
        url = 'https://www.amap.com/service/poiInfo?query_type=TQUERY&pagesize=200&pagenum=' + str(
            i) + '&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=12&geoobj=104.022648%7C30.548945%7C104.218685%7C30.775752&city=510300&keywords=%E8%8A%B1%E5%BA%97'
        html = str(load_page(url), encoding="utf8")
        print(html)
        # 转json
        jsonData = json.loads(html)
        # list
        if "poi_list" in jsonData["data"].keys():
            list = jsonData["data"]["poi_list"]
            for elem in list:
                temp.append(elem)
        else:
            break
        time.sleep(2)

    write_list_to_excel(temp)
    # print(parse_one_page(html))


# 打印到excel
def write_list_to_excel(list, province, city):
    if os.path.exists(province) == False:
        os.mkdir(province)

    # 将sql作为参数传递调用get_data并将结果赋值给result,(result为一个嵌套元组)
    # 实例化一个Workbook()对象(即excel文件)
    wbk = xlwt.Workbook()
    # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    # 获取当前日期，得到一个datetime对象如：(2016, 8, 9, 23, 12, 23, 424000)
    today = datetime.today()
    # 将获取到的datetime对象仅取日期如：2016-8-9
    today_date = datetime.date(today)
    sheet.write(0, 0, "id")
    sheet.write(0, 1, "所在城市")
    sheet.write(0, 2, "花店名称")
    sheet.write(0, 3, "花店电话")
    sheet.write(0, 4, "花店地址")
    sheet.write(0, 5, "经度")
    sheet.write(0, 6, "纬度")
    sheet.write(0, 7, "花店名称")

    # 遍历result中的没个元素。
    for i in range(len(list)):
        # 对result的每个子元素作遍历，
        for j in range(len(list[i])):
            # 将每一行的每个元素按行号i,列号j,写入到excel中。
            sheet.write(i + 1, 0, list[i]["id"])
            sheet.write(i + 1, 1, list[i]["cityname"])
            sheet.write(i + 1, 2, list[i]["name"])
            sheet.write(i + 1, 3, list[i]["tel"])
            sheet.write(i + 1, 4, list[i]["address"])
            sheet.write(i + 1, 5, list[i]["longitude"])
            sheet.write(i + 1, 6, list[i]["latitude"])
            if "disp_name" in list[i].keys():
                sheet.write(i + 1, 7, list[i]["disp_name"])

    # 以传递的name+当前日期作为excel名称保存。
    wbk.save("自贡" + str(today_date) + '.xls')


def load_area():
    areaStr = ""
    with open(r'C:\\Users\\pig\Desktop\area.json', 'r', encoding='UTF-8', errors='ignore') as f:
        for line in f.readlines():
            areaStr += line.strip()
    areaJson = json.loads(areaStr)
    for area in areaJson:
        if area["ParentId"] == 510000:
            print(area["AreaId"], area["Name"])


main()
