#!/usr/bin/env python
# -*- coding:utf-8 -*-
# parse.py  @  2015-08-13 11:10:58
# Author: Fuyuan.CHu 
# Mail: Fuyuan.Chu@emc.com
#########################################################################

import json
import subprocess 
import sys

msg_file = "./message.json"
INPUT = "plugins.input"
OUTPUT = "plugins.output"
EXCHANGE= "plugins.exchange"
f = open(msg_file, "r")
message = json.load(f)

if len(message) is not 3:
    sys.exit(1)

tuple_input = (INPUT+"."+message["input"]["name"], message["input"]["arguments"])
plugin_name = tuple_input[0]
plugin_args = tuple_input[1]

class fileIn(object):
    def __init__(self, filename, lines=5):
        filename = filename
        lines = lines
        print subprocess.Popen(["tail", "-n%s" % lines, filename], stdout=subprocess.PIPE).communicate()[0]
    
def make_arg(tuple_input):
    plugin_name = tuple_input[0]
    plugin_args = tuple_input[1] # list object
    param = {}
    for arg in plugin_args:
        param = dict(arg.items()+param.items())
    res = fileIn(**param)

make_arg(tuple_input)

