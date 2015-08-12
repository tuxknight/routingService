#!/usr/bin/env python

import socket
import os
import logger
from . import BaseExchange


class UnixSocketExchange(BaseExchange):
    """{"module": "exchange",
        "name": "unixsocket",
        "author": "Fuyuan.Chu <fuyuan.chu@emc.com>",
        "version": "0.1",
        "desc": "",
        "options": [
             {"option": "sock",
              "required": false,
              "default": "/tmp/exchange.sock",
              "desc": "unix socket file which server will listen to"
             },
             {"option": "max_conns",
              "required": false,
              "default": 5,
              "desc": "max number of queued connections"
             }
        ]
    }
    """
    def __init__(self, sock="/tmp/exchange.sock", max_conns=5):
        """exchange data with service"""
        super(UnixSocketExchange, self).__init__()
        logger.drs_log.debug("plugin: exchange/UnixSocketExchange")
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock_file = sock
        self.max_conns = max_conns
        if os.path.exists(self.sock_file):
            os.unlink(self.sock_file)
        self.server.bind(self.sock_file)
        self.server.listen(self.max_conns)

    def run(self, data):
        connection, address = self.server.accept()
        logger.drs_log.debug("input data size: %d" % len(data))
        logger.drs_log.debug("new connection accepted")
        stream_out = ""
        try:
            interactor = InteractWithService(connection,
                                             data,
                                             buffer_size=1024)
            stream_out = interactor.exchange()
        except socket.error as e:
            logger.drs_log.warn("socket error (%s)" % e.message)
        finally:
            connection.shutdown(2)
            connection.close()
            return stream_out


class InteractWithService(object):
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


def inject_plugin():
    return UnixSocketExchange
