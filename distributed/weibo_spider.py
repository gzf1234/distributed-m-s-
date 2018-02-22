# -*- coding: utf8 -*-
#user:gzf

import requests
from lxml import etree
from urllib.parse import urljoin
import threading
import re
import time
from pyquery import PyQuery as pq

from heartbeat_client import HeartBeatClient
import protocol_constants as pc
from settings import MAX_PAGE_NUM

root_url = 'http://www.cq.gov.cn/public-wcms-webapp/content/Content!findContentList.action?wcmsSiteTreeSid=10041&pageNo={}&pageSize=15'
base_url = 'http://www.cq.gov.cn/publicinfo/web/views/Show!detail.action?sid=4290481'




HBC = HeartBeatClient()

# def get_urls():
#     global page_break_num, max_page_num
#
#     for page_num in range(1,max_page_num):
#         url = root_url.format(str(page_num))
#         res = requests.get(url)
#         res.encoding = 'utf-8'
#         sel = etree.HTML(res.text)
#         all_urls = sel.xpath('//div[@class="list"]//li/a/@href')
#         urls = []
#         for url in all_urls:
#             new_url = urljoin(base_url, url)
#             urls.append(new_url)
#         print(urls)
#         HBC.finish_target_urls(urls)
#
#
# def get_content():
#
#     urls = dbmanager.dequeueUrls()
#     if urls is None:
#         time.sleep(5)
#     for url in urls:
#         res = requests.get(url)
#         # sel = etree.HTML(res.text)
#         # content = sel.xpath('//div[@class="content"]//*//text()')
#         doc = pq(res.text)
#         content = str(doc('.content'))
#         print(type(content))
#         with open('content.txt', 'w+', encoding='utf-8') as f:
#             f.write(content)
#         print('抓取url: ', url)

def get_page_content(is_root_page):

    # 先获取所有详情页的url
    if is_root_page is True:
        for page_num in range(1, MAX_PAGE_NUM):
            url = root_url.format(str(page_num))
            res = requests.get(url)
            res.encoding = 'utf-8'
            sel = etree.HTML(res.text)
            all_urls = sel.xpath('//div[@class="list"]//li/a/@href')
            urls = []
            for url in all_urls:
                new_url = urljoin(base_url, url)
                urls.append(new_url)
            print(urls)
            HBC.finish_target_urls(urls)

    # 开始抓取详情页的信息
    curtask = HBC.get_target_urls() #type(curtask) = dict
    crawl_delay = curtask.get(pc.CRAWL_DELAY)
    urls = curtask.get(pc.DATA)
    if urls is None:
        time.sleep(5)
    if crawl_delay is not None:
        sleep_time = crawl_delay
    else:
        sleep_time = 0
    for url in urls:
        res = requests.get(url)
        doc = pq(res.text)
        content = str(doc('.content'))
        print(type(content))
        with open('content.txt', 'w+', encoding='utf-8') as f:
            f.write(content)
        print('抓取url: ', url)
        time.sleep(sleep_time)

