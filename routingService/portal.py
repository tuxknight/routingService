#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
import SocketServer
from subprocess import Popen
from subprocess import PIPE
from pluginLoader import PluginManager
from service import InteractWithService

'''
class ThreadedRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        result = ""
        buf = 1024
        raw_data = Popen(["tail", "-n%d" % 50, "/var/log/syslog"],
                         stdout=PIPE).communicate()[0]
        buf_size = len(raw_data)
        self.request.sendall(str(buf_size))
        self.request.recv(1024)
        self.request.sendall(raw_data)
        while True:
            data = self.request.recv(buf)
            if not data:
                break
            result = result + data
        print result


class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.UnixStreamServer):
    pass


server = ThreadedServer("/var/run/exchange.sock", ThreadedRequestHandler)
server_thread = threading.Thread(target=server.serve_forever())
server_thread.daemon = True
server_thread.start()
'''


class Portal:
    """Portal receives data from router, sends to service and then
receives results from service, sends results to router.
Portal interact with service using unix socket while interacting
with router through input and output plugins.
"""
    def __init__(self, plugin_input, plugin_output, service_name):
        """input: input plugin name to load
            output: output plugin name to load
            service_name: service name which Portal interact with
        """
        self.manager = PluginManager()
        self.input = self.manager.get_plugin(plugin_input)()
        self.output = self.manager.get_plugin(plugin_output)()
        self.service_name = service_name

    def work(self):
        stream_in = self.input.run()
        exchange = InteractWithService("/var/run/exchange.sock", stream_in, buffer_size=1024)
        stream_out = exchange.exchange()
        self.output.run(stream_out)


p = Portal("plugins.input.file", "plugins.output.file", "filter")
p.work()
