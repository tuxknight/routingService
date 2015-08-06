#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import os
import multiprocessing
from time import sleep
from threading import Thread


class FilterService(multiprocessing.Process):
    def __init__(self, sock_file, pipe):
        super(FilterService, self).__init__()
        self.raw_data = ""
        self.result = ""
        self.bufsize = 1024
        self.sock_file = sock_file
        self.pipe = pipe

    def _connect(self, sock_file):
        while True:
            if os.path.exists(sock_file):
                self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                try:
                    self.sock.connect(sock_file)
                    print("connecting to %s" % sock_file)
                    break
                except socket.error as e:
                    print("Connection Failed(%s), waiting..." %e)
                    sleep(10)
            else:
                print("Unix socket file %s not found. Waiting for sockets..." % sock_file)
                sleep(10)

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
            self.sock.sendall(self.result)
            self.sock.close()

    def run(self):
        self._connect(self.sock_file)
        self._receive()
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
    # data_queue = multiprocessing.Queue(200)
    while True:
    # TODO: move socket.connect outside of FilterService, so the main loop
    #   could be blocked by socket waiting connections
        (socket_client, worker_pipe) = multiprocessing.Pipe(duplex=True)
        service = FilterService("/var/run/exchange.sock", socket_client)
        worker = Worker(worker_pipe)
        service.start()
        worker.start()
        sleep(2)

