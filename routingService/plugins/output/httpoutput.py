#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import BaseOutput
import logger

class HttpOutput(BaseOutput):
    def run(self, data):
        """deal with output type: Http
        send data"""
        logger.drs_log.debug("plugin: output/HttpOutput")
        print("sending %s" %data)


def inject_plugin():
    return HttpOutput
