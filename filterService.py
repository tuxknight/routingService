#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

class BaseService(object):
    def __init__(self, sock_file="/var/run/exchange.sock"):
        self.sock_file = sock_file
        self.sock = socket.socket(socket.AF_UNSPEC, socket.SOCK_STREAM)
        self.raw_data = ""
        self.result = ""


class FilterService(BaseService):
    def __init__(self):
        super(FilterService, self).__init__()
        self.name = "filter"

    def _connect(self, stop=False):
        self.conn = self.sock.connect(self.sock_file)
        if stop:
            self.conn.close()

    def _receive(self):
        self.conn.send(self.name)
        while True:
            data = self.conn.recv(2048)
            if not data: break
            self.raw_data = self.raw_data + data

    def _worker(self):
        if self.raw_data:
            self.result = self.raw_data.upper()
            return 1
        else:
            return -1

    def _send(self):
        if self.result:
            self.conn.sendall(self.result)

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

