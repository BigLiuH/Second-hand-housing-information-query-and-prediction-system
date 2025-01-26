import requests
from bs4 import BeautifulSoup as bs
import re
import os, sys

import time
import random
import csv

# 设置 CSV 文件头部
header = ['房屋信息链接', '房屋地址', '户型', '房屋面积', '朝向', '装修', '楼层', '年份', '房屋类型', '价格', '城市']

# 设置 CSV 文件路径
csv_file = '重庆.csv'

# 如果文件不存在，写入标题行
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/92.0",
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6',
    'Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
    # Add more user agents here
]
s = requests.session()
s.keep_alive = False
requests.adapters.DEFAULT_RETRIES = 5
headers_ = {
    "User-Agent": random.choice(user_agents),

    "cookie": "lianjia_uuid=e2b91d4e-7318-488e-bab6-6955dff94fcc; sajssdk_2015_cross_new_user=1; crosSdkDT2019DeviceId=-avg8s4-8pbec2-tj8ltli43sst92b-kdnd9aqfa; lianjia_token=2.00141693c743cd194505bbbaf6bb65e00a; lianjia_token_secure=2.00141693c743cd194505bbbaf6bb65e00a; security_ticket=MliAp3Vdhir80Av98ZF/EIUwviBx8Cblw8JWdXTO91VRdmTjiUoGbiYmZTOOu2IQpY5aq8elDhvXxVYU6MYTmAIW50y+WVD9PoH7rFBRUgBc2BdL0Zsf8dRaO4sz6MU6ir8YVH6Ynx6KMTT2AgeIS86D2wgd3MbDEi3coI+Ki3U=; lianjia_ssid=23155794-d671-436b-ba78-c0d31c66354e; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219384e06a46620-08870e7283dbd3-4c657b58-1354896-19384e06a47284f%22%2C%22%24device_id%22%3A%2219384e06a46620-08870e7283dbd3-4c657b58-1354896-19384e06a47284f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; select_city=210100",
    'Connection': 'close',
    "referer": "https://sy.lianjia.com/ershoufang/",
}
citys = {"重庆":"cq"}
for city, s in citys.items():
    for i in range(1, 31):
        baseurl: str = (
            f"https://{s}.lianjia.com/ershoufang/pg{"" if i == 1 else i}/"
        )
        html = requests.get(url=baseurl, headers=headers_, stream=True)

        houseinfo = bs(html.text, "html.parser")
        # print(houseinfo)
        rooms = houseinfo.find_all("div", class_="info clear")
        # print(rooms)
        for room in rooms:
            name = room.find("div", class_="title").text
            link = room.find("a").get("href")
            address = room.find("div", class_="positionInfo").text
            price = room.find("div", class_="priceInfo").text
            price = re.search(r"\d+(\.\d+)?", price).group()
            infos = room.find("div", class_="houseInfo").text
            infos = infos.split('|')
            if len(infos) == 7:
                style = infos[0]
                area = re.search(r"\d+", infos[1]).group() if re.search(r"\d+", infos[1]) else None
                towards = infos[2]
                decoration = infos[3]
                floor = infos[4]
                years = re.search(r"\d+", infos[5]).group() if re.search(r"\d+", infos[5]) else None
                building_type = infos[6]
            else:
                style = infos[0]
                area = re.search(r"\d+", infos[1]).group() if re.search(r"\d+", infos[1]) else None
                towards = infos[2] if infos[2] else None
                decoration = infos[3] if infos[3] else None
                floor = infos[4] if infos[4] else None
                years = "暂无数据"
                building_type = infos[5] if infos[5] else None
            print(link, address, style, area, towards, decoration, floor, years, building_type, price)
            # 将数据写入 CSV 文件
            with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    [link, address, style, area, towards, decoration, floor, years, building_type, price, city])
        time.sleep(random.randint(5, 10))