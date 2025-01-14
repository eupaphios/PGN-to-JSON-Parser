#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import chess.pgn
import re
import sys
import pymongo

import os.path
import pathlib
import logging
from datetime import datetime
import sys, traceback

log = logging.getLogger().error
myclient = pymongo.MongoClient("mongodb://root:rootpassword@localhost:27017/")
mydb = myclient["chess"]
mycol = mydb["developers"]


for i in [1, 2]:
    dir_ = sys.argv[i]
    if not os.path.exists(dir_):
        raise Exception(dir_ + ' not found')

is_join = False
if len(sys.argv) == 4:
    if sys.argv[3] == 'join':
        is_join = True


inp_dir = pathlib.Path(sys.argv[1])


def get_file_list(local_path):
    tree = os.walk(str(local_path))
    file_list = []
    out = []
    test = r'.+pgn$'
    for i in tree:
        file_list = i[2]

    for name in file_list:
        if(len(re.findall(test, name))):
            out.append(str(local_path / name))
    return out


def get_data(pgn_file):
    countd = 0
    node = chess.pgn.read_game(pgn_file)

    while node is not None:
        data = node.headers
        data["moves"] = []
        countd += 1
        
        while node.variations:
            next_node = node.variation(0)
            data["moves"].append(
                    re.sub("\{.*?\}", "", node.board().san(next_node.move)))
            node = next_node

        node = chess.pgn.read_game(pgn_file)

        out_dict = {}

        for key in data.keys():
                if key == 'Result':
                    out_dict['Result'] = result(data.get('Result'))
                if key == 'moves':
                    out_dict['moves'] = data.get('moves')

        mongo_write(out_dict)
        log('insert'+' '+str(countd))

def mongo_write(out_dict):
    mycol.insert_one(out_dict)

def result(result):
    if result == '1-0':
        return "w"
    elif result == '0-1':
        return "b"
    else:
        return "d"

def convert_file(file_path):
    log('convert file '+file_path.name)
    pgn_file = open(str(file_path), encoding='ISO-8859-1')
    get_data(pgn_file)




file_list = get_file_list(inp_dir)

start_time = datetime.now()
for file in file_list:
    convert_file(pathlib.Path(file))


end_time = datetime.now()
log('time '+str(end_time-start_time))
