#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import os


class InteractWithService:
    def __init__(self, sock_file, data, buffer_size=1024):
        self.sock_file = sock_file
        self.raw_data = data
        self.data_sent = False
        self.result_received = False
        self.result = ""
        self.buf = buffer_size
        self.portal_server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    def _get_connection(self, max_conns):
        if os.path.exists(self.sock_file):
            os.unlink(self.sock_file)
        self.portal_server.bind(self.sock_file)
        self.portal_server.listen(max_conns)

    def start(self):
        self._get_connection(5)
        connection, address = self.portal_server.accept()
        buf_size = len(self.raw_data)
        connection.sendall(str(buf_size))
        response = connection.recv(1024)
        if response == "start":
            connection.sendall(self.raw_data)
            result_size = connection.recv(1024)
            result_size = int(result_size)
            connection.sendall("start")
            print("recieving...")
            for x in range(result_size//self.buf):
                data = connection.recv(self.buf)
                self.result = self.result + data
                result_size -= self.buf
            self.result = self.result + connection.recv(result_size)

    def exchange(self):
        self.start()
        return self.result


if __name__ == "__main__":
    pass
