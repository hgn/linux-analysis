#!/usr/bin/python3

import os
import sys
import json
import pprint
import copy


def calc_delta(db_before, db_after):
    delta_db = copy.deepcopy(db_before)
    for cpu, cpu_data in db_before.items():
        for state, state_data in cpu_data.items():
            delta_db[cpu][state]["usage"] = db_after[cpu][state]["usage"] - db_before[cpu][state]["usage"]
            delta_db[cpu][state]["time"] = db_after[cpu][state]["time"] - db_before[cpu][state]["time"]
    return delta_db


if len(sys.argv) < 4:
    print(f"usage: {sys.argv[0]} <before.json> <after.json> <new-delta.json>")
    sys.exit(1)

def read_data(filename):
    with open(filename) as fd:
        return json.load(fd)

def write_json(filename, data):
    with open(filename, "w") as fd:
        json.dump(data, fd)


d_before = read_data(sys.argv[1])
d_after = read_data(sys.argv[2])
delta = calc_delta(d_before, d_after)
write_json(sys.argv[3], delta)





