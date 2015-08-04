#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import os
from time import sleep
from threading import Thread

class BaseService(object):
    def __init__(self, sock_file="/var/run/exchange.sock"):
        self.sock_file = sock_file


class FilterService(BaseService):
    def __init__(self):
        super(FilterService, self).__init__()
        self.name = "filter"
        self.raw_data = ""
        self.result = ""

    def _connect(self, stop=False):
        if stop:
            self.sock.close()
            return 0
        while True:
            if os.path.exists(self.sock_file):
                self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                try:
                    self.sock.connect(self.sock_file)
                    print("connecting to %s" %self.sock_file)
                    break
                except socket.error as e:
                    print("Connection Failed(%s), waiting..." %e)
                    sleep(10)
            else:
                #raise Exception("Unix socket file %s not found." %self.sock_file)
                print("Unix socket file %s not found. Waiting for sockets..." %self.sock_file)
                sleep(10)

    def _receive(self):
        print("handshake...")
        self.sock.send(self.name)
        while True:
            print("receiving data...")
            data = self.sock.recv(1024)
            #if not data: break
            self.raw_data = self.raw_data + data
            break

    def _worker(self):
        if self.raw_data:
            self.result = self.raw_data.upper()
            return 1
        else:
            return -1

    def _send(self):
        if self.result:
            self.sock.sendall(self.result)

    def perform(self):
        self._connect()
        self._receive()
        status = self._worker()
        if status < 0:
            print("Empty data!")
            return -1
        self._send()
        self._connect(stop=True)


if __name__ == "__main__":
    service = FilterService()
    service.perform()
