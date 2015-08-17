#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import multiprocessing
import os
import socket
from time import sleep

from routingService import logger


class FilterService(multiprocessing.Process):
    def __init__(self, connection, pipe, data_size):
        super(FilterService, self).__init__()
        logger.drs_log.info("FilterService start")
        self.raw_data = ""
        self.result = ""
        self.bufsize = 1024
        self.sock = connection
        self.pipe = pipe
        self.status = 0
        self.size = int(data_size)

    def _receive(self):
        logger.drs_log.debug("%s" % self.sock.getsockname())
        #size = self.sock.recv(1024)
        logger.drs_log.debug("raw data size: %s" % self.size)
        self.sock.sendall("start")
        for x in range(self.size//self.bufsize):
            """if size little than self.bufsize, this will not run"""
            data = self.sock.recv(self.bufsize)
            self.raw_data = self.raw_data + data
            self.size -= self.bufsize
        self.raw_data = self.raw_data + self.sock.recv(self.size)

    def _valve(self):
        if self.raw_data:
            logger.drs_log.debug("write to pipe")
            self.pipe.send(self.raw_data)
            try:
                logger.drs_log.debug("try recv from pipe")
                self.result = self.pipe.recv()
            except EOFError as e:
                logger.drs_log.warn("Pipe error(%s)" % e.message)
            finally:
                logger.drs_log.debug("Pipe close")
                self.pipe.close()

    def _send(self):
        if self.result:
            logger.drs_log.debug("sending result...")
            data_size = len(self.result)
            self.sock.sendall(str(data_size))
            response = self.sock.recv(1024)
            if response == "start":
                self.sock.sendall(self.result)
            self.sock.close()

    def run(self):
        try:
            self._receive()
        except socket.error as e:
            self.status = -1
            return 
        self._valve()
        self._send()


class Worker(multiprocessing.Process):
    def __init__(self, pipe):
        super(Worker, self).__init__()
        logger.drs_log.info("Worker start")
        self.pipe = pipe
        self.md5sum = hashlib.md5()

    def run(self):
        logger.drs_log.debug("worker receive from pipe")
        try:
            raw_data = self.pipe.recv()
            logger.drs_log.info("worker calculating...")
            self.md5sum.update(raw_data)
            self.pipe.send(self.md5sum.hexdigest())
        except EOFError as e:
            logger.drs_log.warn("pipe error(%s)" % e.message)
        finally:
            self.pipe.close()

if __name__ == "__main__":
    def get_connection(sockfile):
        while True:
            if os.path.exists(sockfile):
            #if True:
                #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                try:
                    logger.drs_log.debug("get connection")
                    sock.connect(sockfile)
                    return sock
                except socket.error as e:
                    #pass
                    logger.drs_log.warn("Connection Failed(%s), waiting..." % e)
                    sleep(10)
            else:
                logger.drs_log.warn("Unix socket file %s not found. Waiting for sockets..." % sockfile)
                sleep(10)

    sock_file = "/tmp/exchange.sock"
    # sock_file = ("127.0.0.1", 6003)
    while True:
        conn = get_connection(sock_file)
        (client_pipe, worker_pipe) = multiprocessing.Pipe(duplex=True)
        try:
            size = conn.recv(1024)
        except socket.error as e: 
            logger.drs_log.debug("Connection closed(%s)" % e)
        if size:
            service = FilterService(conn, client_pipe, size)
            size = ""  # reset size
            worker = Worker(worker_pipe)
            service.daemon = True
            worker.daemon = True
            service.start()
            logger.drs_log.info("Service process id:%s" % service.ident)
            worker.start()
            logger.drs_log.info("Worker process id:%s" % worker.ident)
            worker.join()
            service.join()
