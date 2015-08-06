#!/usr/bin/env python
# -*- coding: utf-8 -*-


from . import BaseInput
from subprocess import PIPE
from subprocess import Popen


class FileIn(BaseInput):
    def run(self):
        """deal with input type: file
        return data"""
        print("plugin: input/file")
        print("reading files from routing service")
        return self.read("/var/log/syslog", 5)

    def read(self, filename, lines):
        return Popen(["tail", "-n%d" % lines, filename],
                     stdout=PIPE).communicate()[0]


def inject_plugin():
    return FileIn
