#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import os
import multiprocessing
from time import sleep


class FilterService(multiprocessing.Process):
    def __init__(self,connection, pipe):
        super(FilterService, self).__init__()
        self.raw_data = ""
        self.result = ""
        self.bufsize = 1024
        self.sock= connection
        self.pipe = pipe
        self.status = 0

    def _receive(self):
        size = self.sock.recv(1024)
        print("raw data size: %s" % size)
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
            self.pipe.send(self.raw_data)
            try:
                self.result = self.pipe.recv()
            except EOFError as e:
                print("Pipe error(%s)" % e.message)
            finally:
                self.pipe.close()

    def _send(self):
        if self.result:
            print("sending result...")
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
        self.pipe = pipe

    def run(self):
        raw_data = self.pipe.recv()
        self.pipe.send(raw_data.upper())
        self.pipe.close()

if __name__ == "__main__":
    def get_connection(sockfile):
        while True:
            if os.path.exists(sockfile):
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                try:
                    sock.connect(sockfile)
                    print("connecting to %s" % sockfile)
                    return sock
                except socket.error as e:
                    print("Connection Failed(%s), waiting..." %e)
                    sleep(10)
            else:
                print("Unix socket file %s not found. Waiting for sockets..." % sockfile)
                sleep(10)

    sock_file = "/var/run/exchange.sock"
    while True:
        conn = get_connection(sock_file)
        (client_pipe, worker_pipe) = multiprocessing.Pipe(duplex=True)
        service = FilterService(conn, client_pipe)
        worker = Worker(worker_pipe)
        service.daemon = True
        worker.daemon = True
        service.start()
        worker.start()
        worker.join()
        service.join()
