# -*- coding: utf-8 -*-
import random

from bs4 import BeautifulSoup
import urllib.request
from fake_useragent import UserAgent
import requests
import os
import re
import time

from internal.common.func import url_encode


#
def read_spider_it_home(request):
    it_url = "https://m.ithome.com"

    # 随机agent
    def get_random_user_agent():
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
        ]
        return random.choice(agents)

    # 完整的heads参数
    headers = {
        'User-Agent': get_random_user_agent,
         #接受的内容类型
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        # 连接设置
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        # 安全设置
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        # 其他
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',  # Do Not Track
    }

    #
    array = []
    #
    try:
        # 获取网页
        response = urllib.request.urlopen(it_url)
        # req = urllib.request.Request(it_url, headers=headers)
        # response = urllib.request.urlopen(req)
        html = response.read().decode("utf-8")  # 编码格式gb2312,utf-8,GBK
        html_string = str(html)  # 转换成string，可以直接向数据库添加
        soup = BeautifulSoup(html_string, "html.parser")  # 解析网页标签
        # 解析数据
        news_array = soup.find_all("div", attrs={"class", "placeholder"})
        index = 0 #
        for a_news in news_array:
            news_id = a_news.get("data-news-id")
            news_href = a_news.find("a").get("href")
            news_title = a_news.find("p", attrs={"class", "plc-title"}).get_text()
            news_time = a_news.find("span", attrs={"class", "post-time"}).get_text()
            comments_num = a_news.find("span", attrs={"class", "review-num"}).get_text().replace("评", "")
            info = {
                "news_index": index,
                "news_id": news_id,
                "news_href": news_href,
                "news_title": url_encode(news_title),
                "news_time": news_time,
                "comments_num": comments_num,
            }
            array.append(info)
            index = index + 1
            pass
        #
        state = 1
        msg = "完成"
        pass
    except:
        state = 0
        msg = "数据错误"
        pass

    #
    return {
        "state": state,
        "msg": msg,
        "content": {
            "it_url": it_url,
            "array": array,
        },
    }