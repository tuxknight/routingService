#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pluginLoader import PluginManager
from service import InteractWithService
import logger


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
        logger.drs_log.info("Start data exchange")
        exchange = InteractWithService("/tmp/exchange.sock", stream_in, buffer_size=1024)
        stream_out = exchange.exchange()
        logger.drs_log.info("Finish data exchange.")
        self.output.run(stream_out)


p = Portal("plugins.input.file", "plugins.output.file", "filter")
p.work()
