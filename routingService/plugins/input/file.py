#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from routingService.plugins.input import BaseInput
from . import BaseInput


class FileIn(BaseInput):
    def run(self):
        """deal with input type: file
        return data"""
        print("plugin: input/file")
        print("reading files from routing service")
        #return data

def inject_plugin():
    return FileIn
