#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import os
import logger


class InteractWithService:
    def __init__(self, connection, data, buffer_size=1024):
        self.raw_data = data
        self.data_sent = False
        self.result_received = False
        self.result = ""
        self.buf = buffer_size
        self.connection = connection

    def start(self):
        buf_size = len(self.raw_data)
        logger.drs_log.debug("send size:%d" % buf_size)
        self.connection.sendall(str(buf_size))
        response = self.connection.recv(1024)
        if response == "start":
            self.connection.sendall(self.raw_data)
            result_size = self.connection.recv(1024)
            result_size = int(result_size)
            self.connection.sendall("start")
            logger.drs_log.debug("receiving...")
            for x in range(result_size//self.buf):
                data = self.connection.recv(self.buf)
                self.result = self.result + data
                result_size -= self.buf
            self.result = self.result + self.connection.recv(result_size)

    def exchange(self):
        self.start()
        return self.result


if __name__ == "__main__":
    pass
