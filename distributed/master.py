# -*- coding: utf8 -*-
#user:gzf

import protocol_constants as pc
from socket_server import ServerSocket
from mongo_redis_mgr import MongoRedisUrlManager
from settings import PERIODICAL_CHECK_TIME

import json
import time
import sys
import signal
import threading

constants = {
        'reorder_period': 1200, # client掉线后，默认20min后尝试再连接
        'connection_lost_period': 30, # 30s
}

class CrawlMaster(object):
    # 客户端注册表,{'client_id': {'time':'xx', 'status':'xx'}}
    clients = {}

    server_status = pc.STATUS_RUNNING

    last_rereoder_time = time.time()

    dbmanager = MongoRedisUrlManager()

    def __init__(self, mongo_client=None, mongo_host='127.0.0.1'):
        self.server = ServerSocket(self.on_message)
        self.server.start()

    def on_message(self, msg):
        #msg 是client发送过来的心跳信息
        request = json.loads(msg)
        type = request[pc.MSG_TYPE]
        client_state = {}
        response = {}
        response[pc.SERVER_STATUS] = self.server_status
        if type == pc.REGISTER:
            client_id = self.get_free_id()
            client_state['status'] = pc.STATUS_RUNNING
            client_state['time'] = time.time()
            self.clients[client_id] = client_state
            return client_id
        elif type == pc.UNREGISTER:
            client_id = request.get(pc.CLIENT_ID)
            del self.clients[client_id]
            return json.dumps(response)
        elif type == pc.LOCATIONS:
            crawl_urls = self.dbmanager.dequeueUrls(size=pc.REQUEST_SIZE)
            response[pc.MSG_TYPE] = pc.LOCATIONS
            response[pc.CRAWL_DELAY] = pc.CRAWL_DELAY_TIME
            response[pc.DATA] = crawl_urls
            self.flash_hbtime(request)
            return json.dumps(response)
        elif type == pc.TRIPLES:
            crawl_urls = self.dbmanager.dequeueUrls(request[pc.REQUEST_SIZE])
            response[pc.MSG_TYPE] = pc.LOCATIONS
            response[pc.DATA] = crawl_urls
            self.flash_hbtime(request)
            return json.dumps(response)
        elif type == pc.FINISHED_ITEMS:
            # new urls from client save to db by master
            save_urls = request.get(pc.FINISHED_ITEMS)
            self.dbmanager.enqueueUrls(save_urls)
            self.flash_hbtime(request)
            return json.dumps(response)


        client_id = request.get(pc.CLIENT_ID)
        if client_id is None:
            response[pc.ERROR] = pc.ERR_NOT_FOUND
            return json.dumps(response)
        if type == pc.HEARTBEAT:
            if self.server_status is not self.clients[client_id]['status']:
                if self.server_status == pc.STATUS_RUNNING:
                    response[pc.ACTION_REQUIRED] = pc.RESUME_REQUIRED
                elif self.server_status == pc.STATUS_PAUSED:
                    response[pc.ACTION_REQUIRED] = pc.PAUSE_REQUIRED
                elif self.server_status == pc.STATUS_SHUTDOWN:
                    response[pc.ACTION_REQUIRED] = pc.SHUTDOWN_REQUIRED
                return json.dumps(response)
            else:
                # a normal heart beat
                self.flash_hbtime(request)
                return json.dumps(response)
        else:
            if type == pc.PAUSED:
                client_state['status'] = pc.STATUS_PAUSED
            elif type == pc.RESUMED:
                client_state['status'] = pc.STATUS_RUNNING
            client_state['time'] = time.time() #flash hb time
            self.clients[client_id] = client_state

            return json.dumps(response)

    def periodical_check(self):
        # check heart beat
        # clients_status_ok = True
        while True:
            lost_cid = []
            for cid, state in self.clients.items():
                if time.time() - state['time'] > constants['connection_lost_period']:
                    # del self.clients[cid] -> reason:dictionary changed size during iteration
                    self.clients[cid]['status'] = pc.STATUS_CONNECTION_LOST
                    lost_cid.append(cid)
                    continue

            for cid in lost_cid:
                if self.clients[cid]['status'] != self.server_status:
                    # remove if from client list
                    del self.clients[cid]

            time.sleep(PERIODICAL_CHECK_TIME)


    def get_free_id(self):
        i = 0
        for key in self.clients:
            if i < int(key):
                break
            i += 1
        return str(i)

    def flash_hbtime(self, request):
        client_id = request.get(pc.CLIENT_ID)
        self.clients[client_id]['time'] = time.time()

def exit_signal_handler(signal, frame):
    crawl_master.server.close()
    sys.exit(1)

def server_close():
    crawl_master.server.close()
    sys.exit(1)

crawl_master = CrawlMaster()
#创建一个新线程用于心跳检查
t = threading.Thread(target=crawl_master.periodical_check, name='preiodical_check_thread')
t.start()
# threading._start_new_thread(crawl_master.periodical_check, ())
# signal.signal(signal.SIGINT, exit_signal_handler)
# signal.pause() # wait until a signal arrives [Unix only]


