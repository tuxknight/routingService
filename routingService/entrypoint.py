#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import os
import select
import multiprocessing
from pluginLoader import PluginManager
import logger


class EntryPoint:
    """Portal receives data from router, sends to service and then
receives results from service, sends results to router.
Portal interact with service using unix socket while interacting
with router through input and output plugins.
"""
    def __init__(self, plugin_input, plugin_output, plugin_exchange):
        """input: input plugin name to load
            output: output plugin name to load
            service_name: service name which Portal interact with
        """
        self.manager = PluginManager()
        self.input = self.manager.get_plugin(plugin_input)()
        self.output = self.manager.get_plugin(plugin_output)()
        self.exchanger = self.manager.get_plugin(plugin_exchange)(sock="/tmp/exchange.sock", max_conns=5)

    def start(self):
        flist = ("/var/log/syslog", "/var/log/auth.log", "/var/log/kern.log")
        loop = len(flist)
        while loop>=1:
            logger.drs_log.debug("loop %d" % loop)
            stream_in = self.input.run(flist[loop-1], loop)
            stream_out = self.exchanger.run(stream_in)
            self.output.run(stream_out)
            logger.drs_log.debug("result %s\n" % stream_out)
            loop -= 1

if __name__ == "__main__":
    p = EntryPoint("plugins.input.file", "plugins.output.file", "plugins.exchange.unixsocket")
    p.start()
