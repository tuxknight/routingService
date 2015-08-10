#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import os
import multiprocessing
import hashlib
from time import sleep
from routingService import logger


class FilterService(multiprocessing.Process):
    def __init__(self, connection, pipe):
        super(FilterService, self).__init__()
        logger.drs_log.debug("FilterService start")
        self.raw_data = ""
        self.result = ""
        self.bufsize = 1024
        self.sock = connection
        self.pipe = pipe
        self.status = 0

    def _receive(self):
        logger.drs_log.debug("(%s,%d)" % self.sock.getpeername())
        size = self.sock.recv(1024)
        logger.drs_log.debug("raw data size: %s" % size)
        self.sock.sendall("start")
        size = int(size)
        for x in range(size//self.bufsize):
            """if size little than self.bufsize, this will not run"""
            data = self.sock.recv(self.bufsize)
            self.raw_data = self.raw_data + data
            size -= self.bufsize
        self.raw_data = self.raw_data + self.sock.recv(size)

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
            self.sock.shutdown(2)
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
        logger.drs_log.debug("Worker start")
        self.pipe = pipe
        self.md5sum = hashlib.md5()

    def run(self):
        logger.drs_log.debug("worker receive from pipe")
        try:
            raw_data = self.pipe.recv()
            logger.drs_log.debug("worker calculating...")
            self.md5sum.update(raw_data)
            self.pipe.send(self.md5sum.hexdigest())
        except EOFError as e:
            logger.drs_log.warn("pipe error(%s)" % e.message)
        finally:
            self.pipe.close()

if __name__ == "__main__":
    sock_file = ("127.0.0.1", 6003)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(sock_file)
    sock.listen(5)
    while True:
        logger.drs_log.debug("listening ...")
        connection, address = sock.accept()
        logger.drs_log.debug("accept(%s,%d)" % connection.getpeername())
        (client_pipe, worker_pipe) = multiprocessing.Pipe(duplex=True)
        service = FilterService(connection, client_pipe)
        worker = Worker(worker_pipe)
        service.daemon = True
        worker.daemon = True
        service.start()
        logger.drs_log.debug("Service process id:%s" % service.ident)
        worker.start()
        logger.drs_log.debug("Worker process id:%s" % worker.ident)
        #worker.join()
        #service.join()
