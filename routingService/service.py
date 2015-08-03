#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import PIPE
from subprocess import Popen
import socket
import os

class InteractWithService(object):
    def __init__(self, sock_file, service, data):
        self.sock_file = sock_file
        self.service = service
        self.raw_data = data
        self.data_sent = False
        self.result_received = False
        self.result = ""
        self.portal_server = socket.socket(socket.AF_UNSPEC, socket.SOCK_STREAM)

    def _get_connection(self, max_conns):
        if os.path.exists(self.sock_file):
            os.unlink(self.sock_file)
        self.portal_server.bind(self.sock_file)
        self.portal_server.listen(max_conns)

    def start(self):
        self._get_connection(5)
        conn_status = ""
        while True:
            connection, address = self.portal_server.accept()
            handshake = connection.recv(1024)
            if handshake.startswith(self.service):
                conn_state = 1
                connection.send("START DATA\n\n")
                connection.send(self.raw_data)
                connection.send("END DATA\n\n")
                print("Start to receive results")
                result_data = connection.recv(2048)
                if not result_data: break
                self.result = self.result + result_data
            else:
                print("No service matched to %s" %self.service)
                conn_status = -1
                break
        return conn_status

    def exchange(self):
        status = self.start()
        if status == 1:
            return self.result
        else:
            raise Exception("Exchange Error")


if __name__ == "__main__":
    pass
