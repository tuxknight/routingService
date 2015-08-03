#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import BaseOutput


class HttpOutput(BaseOutput):
    def run(self, data):
        """deal with output type: Http
        send data"""
        print("plugin: output/HttpOutput")
        print("sending %s" %data)

def inject_plugin():
    return HttpOutput
