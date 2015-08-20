#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pluginLoader import PluginManager
import logger


class EntryPoint:
    """Portal receives data from router, sends to service and then
receives results from service, sends results to router.
Portal interact with service using unix socket while interacting
with router through input and output plugins.
"""
    def __init__(self, tuple_input, tuple_output, tuple_exchange):
        """:parameter: tuple_input - a tuple object contains plugin name
        and arguments of that plugin. Plugin name is required and
        arguments are optional.
           :parameter: tuple_output - a tuple object contains plugin name
        and arguments of that plugin. Plugin name is required and
        arguments are optional.
           :parameter: tuple_exchange - a tuple object contains plugin name
        and arguments of that plugin. Plugin name is required and
        arguments are optional.
        """
        assert isinstance(tuple_input, tuple)
        assert isinstance(tuple_output, tuple)
        assert isinstance(tuple_exchange, tuple)
        self.plugin_input = tuple_input[0]
        self.plugin_output = tuple_output[0]
        self.plugin_exchange = tuple_exchange[0]
        if len(tuple_input) is 2:
            self.input_args = tuple_input[1]
        if len(tuple_input) is 2:
            self.output_args = tuple_output[1]
        if len(tuple_input) is 2:
            self.exchange_args = tuple_exchange[1]
        # Get input, output and exchange classes.
        # Instantiation will be performed after arguments are verified.
        self.manager = PluginManager()
        self.PluginInput = self.manager.get_plugin(self.plugin_input)
        self.PluginOutput = self.manager.get_plugin(self.plugin_output)
        self.PluginExchange = self.manager.get_plugin(self.plugin_exchange)

    def start(self):
        """start to work, transport data to services and get all result"""
        # verify arguments first
        self.input_plugin = self.PluginInput(**self.input_args)
        self.output = self.PluginOutput(**self.output_args)
        self.exchanger = self.PluginExchange(**self.exchange_args)
        stream_in = self.input_plugin.run()
        # logger.drs_log.debug(stream_in)
        self.output.run(self.exchanger.run(self.input_plugin.run()))

    def _verify_args(self):
        """Verify all input arguments"""
        json.loads(self.input_args)  # arguments received from agent
        json.loads(self.PluginInput.__doc__)  # plugin's doc string

        json.loads(self.output_args)  # arguments received from agent
        json.loads(self.PluginOutput.__doc__)  # plugin's doc string

        json.loads(self.exchange_args)  # arguments received from agent
        json.loads(self.PluginExchange.__doc__)  # plugin's doc string

if __name__ == "__main__":
    pass
