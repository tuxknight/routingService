#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pluginLoader import PluginManager
from service import InteractWithService


manager = PluginManager("routingService")
input = manager.get_plugin('plugins.input.file')()
#output = manager.get_plugin('plugins.output.httpoutput')()
output = manager.get_plugin('plugins.output.file')()
raw_data = input.run()
#raw_data = "hello"
exchange = InteractWithService("/var/run/exchange.sock", "filter", raw_data)
result = exchange.exchange()
output.run(result)
#print(result)
