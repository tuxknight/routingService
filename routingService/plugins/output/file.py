#!/usr/bin/env python

from . import BaseOutput


class FileOutput(BaseOutput):
    def run(self, data):
        """deal with output type: File
        send data"""
        print("plugin: output/FileOutput")
        print("write data to output.txt")
        self.write("output.txt", data)

    def write(self, filename, content):
        with open(filename, "w") as f:
            f.write(content)

def inject_plugin():
    return FileOutput
