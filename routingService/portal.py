#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import os
import select
import multiprocessing
from pluginLoader import PluginManager
from service import InteractWithService
import logger


class Portal:
    """Portal receives data from router, sends to service and then
receives results from service, sends results to router.
Portal interact with service using unix socket while interacting
with router through input and output plugins.
"""
    def __init__(self, plugin_input, plugin_output, service_name, sock, max_conns):
        """input: input plugin name to load
            output: output plugin name to load
            service_name: service name which Portal interact with
        """
        self.manager = PluginManager()
        self.input = self.manager.get_plugin(plugin_input)()
        self.output = self.manager.get_plugin(plugin_output)()
        self.service_name = service_name
        # self.portal_server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.portal_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_file = sock
        self.max_conns = max_conns
        #if os.path.exists(self.sock_file):
        #    os.unlink(self.sock_file)
        self.portal_server.setblocking(0)
        self.portal_server.bind(self.sock_file)
        self.portal_server.listen(self.max_conns)

    def run(self):
        x = 300
        while x >= 1:
            inputs, outputs, excepts = select.select(
                [self.portal_server], [], [self.portal_server])
            if self.portal_server in inputs:
                connection, address = self.portal_server.accept()
                stream_in = self.input.run()
                logger.drs_log.debug("read data: %d" % len(stream_in))
                logger.drs_log.debug("new connection accepted")
                logger.drs_log.debug("remote addr:(%s,%d)" % connection.getpeername())
                client = multiprocessing.Process(target=self.exchange, args=(connection, stream_in))
                client.daemon = True
                client.start()
                logger.drs_log.debug("Portal thread:%s" % client.ident)
                client.join()
                connection.close()
            x -= 1

    def exchange(self, connection, stream_in):
            logger.drs_log.info("Start data exchange")
            exchange = InteractWithService(connection, stream_in, buffer_size=1024)
            stream_out = exchange.exchange()
            logger.drs_log.info("Finish data exchange.")
            self.output.run(stream_out)


#p = Portal("plugins.input.file", "plugins.output.file", "filter", "/tmp/exchange.sock", 50)
p = Portal("plugins.input.file", "plugins.output.file", "filter", ("127.0.0.1", 6003), 50)
p.run()
