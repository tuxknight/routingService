#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pluginLoader import PluginManager
from service import InteractWithService

class Portal(object):
    """Portal receives data from router, sends to service and then
receives results from service, sends results to router.
Portal interact with service using unix socket while interacting
with router through input and output plugins.
"""
    def __init__(self, input, output, service_name):
        """input: input plugin name to load
            output: output plugin name to load
            service_name: service name which Portal interact with
        """
        self.manager = PluginManager()
        self.input = self.manager.get_plugin(input)()
        self.output = self.manager.get_plugin(output)()
        self.stream_in = ""
        self.stream_out = ""
        self.service_name = service_name

    def from_routing(self):
        """reads raw data using input plugin"""
        self.stream_in = self.input.run()

    def to_service(self):
        """creates a server to interact with service and exchange data"""
        self.exchange = InteractWithService("/var/run/exchange.sock", self.service_name, self.stream_in)

    def from_service(self):
        """receive result data from service"""
        self.stream_out = self.exchange.exchange()

    def to_routing(self):
        """writes raw data using output plugin"""
        self.output.run(self.stream_out)

    def work(self):
        self.from_routing()
        self.to_service()
        self.from_service()
        self.to_routing()

p = Portal("plugins.input.file", "plugins.output.file", "filter")
p.work()
