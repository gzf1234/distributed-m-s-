# -*- coding: utf8 -*-
#user:gzf

import socket
import threading
import json
import time

import protocol_constants as pc
from socket_client import SocketClient

class HeartBeatClient(object):

    server_status = pc.STATUS_RUNNING
    client_id = -1
    hb_period = 5
    skip_wait = False
    socket_client = SocketClient('192.168.1.105', 9000)

    def __init__(self):
        self.run_heartbeat = True

    def connect(self):
        register_request = {}
        register_request[pc.MSG_TYPE] = pc.REGISTER
        self.client_id = self.socket_client.send(json.dumps(register_request)).decode()
        print('this is the client id :', self.client_id)
        if self.client_id is None:
            raise IOError('Connection Failed!')

    def disconnect(self):
        register_request = {}
        register_request[pc.MSG_TYPE] = pc.REGISTER
        self.socket_client.send(json.dumps(register_request))

    def heartbeat(self):
        while self.run_heartbeat:
            if self.skip_wait is False:
                time.sleep(self.hb_period)
            else:
                self.skip_wait = False
            try:
                hb_request = {}
                hb_request[pc.MSG_TYPE] = pc.HEARTBEAT
                hb_request[pc.CLIENT_ID] = self.client_id
                hb_response_data = self.socket_client.send(json.dumps(hb_request))

                # should be network error
                if hb_response_data is None:
                    continue

                response = json.loads(hb_response_data)

                err = response.get(pc.ERROR)
                if err is not None:
                    # client_id is not register
                    if err == pc.ERR_NOT_FOUND:
                        register_request = {}
                        register_request[pc.MSG_TYPE] = pc.REGISTER
                        self.client_id = self.socket_client.send(register_request).decode()

                        # skip heartbeat period and send next heartbeat immediately
                        self.skip_wait = True
                        self.heartbeat()
                        return
                    return

                action = response.get(pc.ACTION_REQUIRED)
                if action is not None:
                    action_request = {}
                    if action == pc.PAUSE_REQUIRED:
                        action_request[pc.MSG_TYPE] = pc.PAUSED
                    elif action == pc.RESUME_REQUIRED:
                        action_request[pc.MSG_TYPE] = pc.RESUMED
                    elif action == pc.SHUTDOWN_REQUIRED:
                        # stop heartbeat thread
                        return
                    action_request[pc.CLIENT_ID] = self.client_id
                    action_response = self.socket_client.send(json.dumps(action_request))
                    self.server_status = action_response.get(pc.SERVER_STATUS)
                else:
                    # a normal heart beat
                    self.server_status = response[pc.SERVER_STATUS]

            except socket.error as msg:
                print('Send Data Error. Error Code: ' + str(msg[0]) + 'Message' + msg[1])
                self.server_status = pc.STATUS_CONNECTION_LOST

    def get_target_urls(self, type=pc.LOCATIONS):
        '''
        :param type: pc.LOCATIONS or pc.TRIPLES
        '''
        hb_request = {}
        hb_request[pc.MSG_TYPE] = type
        hb_request[pc.CLIENT_ID] = self.client_id
        response = self.socket_client.send(json.dumps(hb_request))
        response = json.loads(response)
        crawl_delay = response.get(pc.CRAWL_DELAY)
        response_dict = {}
        if crawl_delay is not None:
            response_dict[pc.DATA] = response[pc.DATA]
            response_dict[pc.CRAWL_DELAY] = crawl_delay
            return response_dict
        else:
            response_dict[pc.DATA] = response[pc.DATA]
            return response_dict

    def finish_target_urls(self, items, _type=pc.FINISHED_ITEMS):
        '''
        :param items: new url list
        '''
        hb_request = {}
        hb_request[pc.MSG_TYPE] = _type
        hb_request[pc.CLIENT_ID] = self.client_id
        hb_request[pc.FINISHED_ITEMS] = items
        self.socket_client.send(json.dumps(hb_request))




