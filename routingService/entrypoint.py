#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
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
    #def __init__(self, (plugin_input, input_args), (plugin_output, output_args), (plugin_exchange, exchange_args)):
    def __init__(self, plugin_input, plugin_output, plugin_exchange):
        """input: input plugin name to load
            output: output plugin name to load
            service_name: service name which Portal interact with
        """
        #self.plugin_input, self.input_args = (plugin_input, input_args)
        #self.plugin_output, self.output_args = (plugin_output, output_args)
        #self.plugin_exchange, self.exchange_args = (plugin_exchange, exchange_args)
        self.manager = PluginManager()
        #self.input = self.manager.get_plugin(self.plugin_input)()
        #self.output = self.manager.get_plugin(self.plugin_output)()
        #self.exchanger = self.manager.get_plugin(self.plugin_exchange)(sock="/tmp/exchange.sock", max_conns=5)
        self.Input = self.manager.get_plugin(plugin_input)
        self.output = self.manager.get_plugin(plugin_output)()
        self.exchanger = self.manager.get_plugin(plugin_exchange)(sock="/tmp/exchange.sock", max_conns=5)

    def start(self):
        filename = "/var/log/syslog"
        input_args = json.loads(self.Input.__doc__)
        # parse json documentation
        #logger.drs_log.debug(input_args["options"][0]["option"])
        self.input = self.Input(filename)
        stream_in = self.input.run()
        logger.drs_log.debug(stream_in)
        #self.output.run(self.exchanger.run(self.input.run(filename, lines)))
        #self.output.run(stream_out)
        #logger.drs_log.debug("result %s\n" % stream_out)

if __name__ == "__main__":
    p = EntryPoint("plugins.input.file", "plugins.output.file", "plugins.exchange.unixsocket")
    p.start()
