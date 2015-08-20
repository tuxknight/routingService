#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class PluginManager(object):
    def __init__(self):
        """Load plugins for module name from plugins/input and plugins/output
        valid plugin files are end with .py and not start with _ """
        self.plugins_list = []
        self.plugins = {}
        self.load_path = dict(input="plugins/input",
                              output="plugins/output",
                              exchange="plugins/exchange")
        self.install_plugins("input")
        self.install_plugins("output")
        self.install_plugins("exchange")

    def install_plugins(self, mod):
        """checkout the names of all available plugins
        in plugins/input and plugins/output"""
        for filename in os.listdir(self.load_path[mod]):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            plugin_name = os.path.splitext(filename)[0]
            plugin_name = "plugins" + "." + mod + "." + plugin_name
            if plugin_name not in self.plugins_list:
                self.plugins_list.append(plugin_name)

    def load_plugin(self, plugin_name):
        """get a instance of plugin_name if the plugin is available"""
        if plugin_name in self.plugins_list:
            if plugin_name not in self.plugins:
                plugin = __import__(plugin_name, fromlist=[plugin_name])
                self.plugins[plugin_name] = plugin.inject_plugin()

    def get_plugin(self, plugin_name):
        """return the instance of plugin_name if it is loaded"""
        if plugin_name in self.plugins:
            return self.plugins[plugin_name]
        else:
            self.load_plugin(plugin_name)
            return self.plugins[plugin_name]


if __name__ == "__main__":
    pass
