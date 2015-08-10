#!/usr/bin/env python

from . import BaseExchange
import logger


class UnixSocketExchange(BaseExchange):
    def run(self, data):
        """exchange data with service"""
        logger.drs_log.debug("plugin: exchange/UnixSocketExchange")


def inject_plugin():
    return UnixSocketExchange

