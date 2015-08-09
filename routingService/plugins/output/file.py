#!/usr/bin/env python

from . import BaseOutput
import logger


class FileOutput(BaseOutput):
    def run(self, data):
        """deal with output type: File
        send data"""
        logger.drs_log.debug("plugin: output/FileOutput")
        self.write("output.txt", data)

    def write(self, filename, content):
        with open(filename, "w") as f:
            f.write(content)


def inject_plugin():
    return FileOutput
