#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json

#{u'input': {u'name': u'file', u'arguments': [{u'filename': u'/var/log/syslog'}, {u'lines': 5}]}, u'output': {u'name': u'file', u'arguments': [{u'filename': u'/var/log/syslog'}, {u'lines': 5}]}, u'exchange': {u'name': u'unixsocket', u'arguments': [{u'sock': u'/var/run/exchange.sock'}]}}

filename = "/var/log/syslog"
lines = 5
sock = "/var/run/exchange.sock"
# input
arg1 = {"filename": filename}
arg2 = {"lines": lines}
args = [arg1, arg2]
_input = {}
_input['name'] = "file"
_input['arguments'] = args

# exchange
arg1 = {"sock": sock}
args = [arg1]
_exchange = {}
_exchange['name'] = "exchange"
_exchange['arguments'] = args

# output
arg1 = {"filename": filename}
arg2 = {"lines": lines}
args = [arg1, arg2]
_output = {}
_output['name'] = "file"
_output['arguments'] = args

message = {}
message['input'] = _input
message['exchange'] = _exchange
message['output'] = _output

print json.dumps(message,indent=4)
