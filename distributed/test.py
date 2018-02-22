# -*- coding: utf8 -*-
#user:gzf

import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("echo")
# args = parser.parse_args()
#
# print(args.echo)


# parser = argparse.ArgumentParser()
# parser.add_argument("-v", "--verbosity", help='increase output verbosity')
# args = parser.parse_args()
# if args.verbosity:
#     print('verbosity turned on')


# parser = argparse.ArgumentParser()
# parser.add_argument("-v", "--verbose", help="increase output verbosity",
#                     action="store_true")
# args = parser.parse_args()
# if args.verbose:
#     print("verbosity turned on")


# parser = argparse.ArgumentParser()
# parser.add_argument('x', type=int, help="the base")
# args = parser.parse_args()
# answer = args.x ** 2
# print(answer)

# parser = argparse.ArgumentParser(description='calculate x to power of y')
# group = parser.add_mutually_exclusive_group()
# group.add_argument("-v", "--verbose", action="store_true")
# group.add_argument("-q", "--quiet", action="store_true")
# parser.add_argument("x", type=int, help="the base")
# parser.add_argument("y", type=int, help="the exponent")
# args = parser.parse_args()
# answer = args.x**args.y
#
# if args.quiet:
#     print(answer)
# elif args.verbose:
#     print("{} to the power {} equals {}".format(args.x, args.y, answer))
# else:
#     print("{}^{} == {}".format(args.x, args.y, answer))


# import sys
#
# a = 'str'
# try:
#     if b == a:
#         print('ok')
# except Exception:
#     print('chucuo')
#     sys.exit('nishi')
#
#
# print('woshiyige baichu ')
# import _signal

# skip_wait = False
#
# from pymongo import MongoClient
#
# client = MongoClient('localhost', 27017)
#
# db = client.taobao
#
# a = db.item_detail.count()
# print(a)
#

import hashlib

# url = 'https://www.baidu.com'
#
# def test(url):
#     print(type(url))
#     if isinstance(url, str):
#         url = bytes(url, 'utf-8')
#         print(url)
#         # url = url.encode('utf-8')
#         print(type(url))
#     a = hashlib.md5(url)
#     hash = a.hexdigest()
#     print(hash)
#
#
# test(url)

# import threading
# import time
#
# def test():
#     print('i am a thread.')
#     time.sleep(2)
#     print('i am a gzf.')
#     time.sleep(2)
#     print('i am a thread.')
#
# threads = []
#
# while True:
#     while True:
#         for t in threads:
#             if not t.is_alive():
#                 threads.remove(t)
#         if len(threads) >= 1:
#             print('max threads!')
#             time.sleep(10)
#             continue
#         print('创建一个新thread')
#         t = threading.Thread(target=test)
#         threads.append(t)
#         t.setDaemon(True)
#         t.start()
#         time.sleep(1)
#         break

# import json
# items = ['1','2','3']
# def finish_target_urls(items, types='pc.FINISHED_ITEMS'):
#     '''
#     :param items: new url list
#     '''
#     hb_request = {}
#     hb_request['pc.MSG_TYPE'] = types
#     hb_request['pc.CLIENT_ID'] = 'client_id'
#     hb_request['pc.FINISHED_ITEMS'] = items
#     # print(type(hb_request))
#     # print(hb_request)
#     # print(type(json.dumps(hb_request).encode('utf-8')))
#     print(json.dumps(hb_request))
#
#
#
a = b'nihao'
b = str(a)
c = a.decode()
print(c)
print(type(c))
print(b)

print(a)

print(type(a))
print(type(b))

