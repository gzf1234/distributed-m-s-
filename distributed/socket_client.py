# -*- coding: utf8 -*-
#user:gzf

import socket
import sys

class SocketClient(object):
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        # Create a TCP/IP socket
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.connect((self.server_ip, self.server_port))
        # self.families = self.get_constants('AF_')
        # self.types = self.get_constants('SOCK_')
        # self.protocols = self.get_constants('IPPROTO_')

    # def get_constants(self, prefix):
    #     '''Create a dictionary mapping socket module constants to their names.'''
    #     return dict((getattr(socket, n), n)
    #                 for n in dir(socket)
    #                 if n.startswith(prefix)
    #                 )

    def send(self, message):
        # try:
        #     # connect to server
        #     # self.sock = socket.create_connection((self.server_ip, self.server_port))
        #     self.sock.sendall(message.encode('utf-8'))
        #
        #     data = self.sock.recv(1024)
        #     return data
        # except socket.error as msg:
        #     print('Bind failed reason: ', msg)
        #
        # finally:
        #     if hasattr(self, 'sock'):
        #         self.sock.close()

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.server_ip, self.server_port))
                sock.sendall(message.encode('utf-8'))
                data = sock.recv(8192)
                return data
        except socket.error as msg:
            print('Bind failed reason: ', msg)