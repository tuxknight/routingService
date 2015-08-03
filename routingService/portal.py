#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pluginLoader import PluginManager
from service import InteractWithService


manager = PluginManager("routingService")
input = manager.get_plugin('plugins.input.file')()
output = manager.get_plugin('plugins.output.httpoutput')()
raw_data = input.run()
exchange = InteractWithService("/var/run/exchange.sock", "filter", raw_data)
try:
    result = exchange.exchange()
except Exception as e:
    print("%s" %e.message)
output.run(result)
