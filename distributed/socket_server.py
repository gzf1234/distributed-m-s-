# -*- coding: utf8 -*-
#user:gzf

import sys
import socket
import _thread
import threading

import signal

class ServerSocket(object):
    def __init__(self, callback, host='127.0.0.1', port=9000):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.callback = callback

        #Bind socket to localhost and port
        try:
            self.s.bind((host, port))
        except socket.error as msg:
            print('Bind failed.reason: ', msg)
            #退出主程序
            sys.exit()

        #start listening bind socket
        self.s.listen(10)
        #print('socket now listening')

    def startlistening(self):
        #now keep talking with the socket
        while True:
            #wait to accept a connection - blocking call
            conn, addr = self.s.accept()

            #start new thread takes 1st argument as a function,
            # second is the tuple of arguments to the function
            t = threading.Thread(target=self.clientthread, args=(conn,), name='handle_client_thread')
            t.start()

    #Function for handling connection, This will be used to create threads
    def clientthread(self, conn):
        #Sending message to connection client

        data = conn.recv(8192)
        print(data)
        reply = self.callback(data)
        # print(reply)
        #reply 是处理之后需要发给client的信息
        conn.sendall(reply.encode('utf-8'))
        conn.close()

    def start(self):
        t = threading.Thread(target=self.startlistening, name='server_listening_thread')
        t.start()

    def close(self):
        self.s.close()

def msg_received(data):
    return 'Ack'

def exit_signal_handler(signal, frame):
    pass


if __name__ == '__main__':
    server = ServerSocket(msg_received)
    server.start()
    # server.close()
    # sys.exit()


