# -*- coding: utf8 -*-
#user:gzf

import protocol_constants as pc
from socket_client import SocketClient
from mongo_redis_mgr import MongoRedisUrlManager
from heartbeat_client import HeartBeatClient
from settings import MAX_NUM_THREAD, MAX_PAGE_NUM, ROOT_URL, BASE_URL

import json
import time
import threading
import requests
from urllib.parse import urljoin
from lxml import etree
from pyquery import PyQuery as pq


def get_page_content(is_root_page=False):
    # 先获取所有详情页的url
    if is_root_page is True:
        for page_num in range(1, MAX_PAGE_NUM):
            url = ROOT_URL.format(str(page_num))
            res = requests.get(url)
            res.encoding = 'utf-8'
            sel = etree.HTML(res.text)
            all_urls = sel.xpath('//div[@class="list"]//li/a/@href')
            urls = []
            for url in all_urls:
                new_url = urljoin(BASE_URL, url)
                urls.append(new_url)
            print('获取新的待爬取url:', urls)
            HBC.finish_target_urls(urls)

    #  开始抓取详情页的信息
    curtask = HBC.get_target_urls() #  type(curtask) = dict
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


HBC = HeartBeatClient() # create a TCP/IP socket

dbmanager = MongoRedisUrlManager() # db manager

start_time = time.time()
is_root_page = True
threads = [] # spider thread pool
CRAWL_DELAY = 1

register_request = {}
# register_request[pc.MSG_TYPE] = pc.REGISTER
# client_id = socket_client.send(json.dumps(register_request))

#  心跳间隔
#  hb_period = 5
#  run_heartbeat = True
# server_status = pc.STATUS_RUNNING

#  在主线程中尝试将client注册到master上
HBC.connect()

try:
    t = threading.Thread(target=HBC.heartbeat, name='heartbeat_thread')
    #  将主线程设置为守护线程，可以被 ctrl-c 命令退出
    #  子线程会随主线程的结束而结束，程序不会被无限挂起
    t.setDaemon(True)
    t.start()
except Exception:
    print('Error: unable to start heartbeat thread')

while True:
    #  start to check status
    if HBC.server_status == pc.STATUS_PAUSED:
        time.sleep(HBC.hb_period)
        continue
    if HBC.server_status == pc.STATUS_SHUTDOWN:
        HBC.run_heartbeat = False  # stop heartbeat
        #  等待所有爬虫线程退出后再break
        for t in threads:
            t.join()
        break
    # curtask = HBC.get_target_urls() # type(curtask) = dict
    # print('cur task is:' + curtask)

    # if curtask is None:
    #     time.sleep(HBC.hb_period)
    #     continue

    #  looking for an empty thread from pool to crawl

    if is_root_page is True:
        get_page_content(is_root_page)
        is_root_page = False
    else:
        while True:
            # first remove all finished running threads
            for t in threads:
                if not t.is_alive():
                    threads.remove(t)
            if len(threads) >= MAX_NUM_THREAD:
                time.sleep(HBC.hb_period)
                continue
            try:
                # create a new spider thread
                t = threading.Thread(target=get_page_content, name='spider_thread', args=(is_root_page,))
                threads.append(t)
                # set daemon so main thread can exit when receives ctrl-c
                t.setDaemon(True)
                t.start()
                time.sleep(CRAWL_DELAY)
                break
            except Exception:
                print('Error: unable to start thread!')

shutdown_request = {}
shutdown_request[pc.MSG_TYPE] = pc.SHUTDOWN
shutdown_request[pc.CLIENT_ID] = HBC.client_id
HBC.socket_client.send(json.dumps(shutdown_request))