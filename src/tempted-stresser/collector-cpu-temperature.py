#!/usr/bin/python3

import os
import sys
import subprocess
import psutil
import time
import pprint
import collections
import glob
import re
import signal

start_time = time.time()

def difftime():
    return time.time() - start_time

def sigint_handler(sig, frame):
    os.sync()
    fd.close()
    sys.exit(0)

def get_processor_core_id_mapping():
    """ no the shinny python way, but grepping in one line is also nice """
    cmd = "grep 'processor\|core id' /proc/cpuinfo"
    lines = subprocess.check_output(cmd, shell=True, encoding='utf8').split("\n")
    queue = collections.deque(lines)
    db = {}
    while True:
        try:
            first = queue.popleft()
            second = queue.popleft()
        except IndexError:
            break
        (_, processor_id) = first.split(":")
        (_, core_id) = second.split(":")
        id_ = core_id.strip()
        if id_ not in db:
            db[core_id.strip()] = processor_id.strip()
    return db

def read_file(path):
    with open(path, "r") as fd:
        return fd.read().strip()


def read_label(path):
    """ Core 28 -> 28 """
    buf = read_file(path)
    core_id = buf.split()[1].strip()
    if not core_id.isdigit():
        return None
    return core_id
    

def read_temps(processor_core_map):
    db = {}
    for name in glob.glob('/sys/devices/platform/coretemp.*/hwmon/hwmon*/temp*_label'):
        core_id = read_label(name)
        if not core_id:
            continue
        processor_id = int(processor_core_map[core_id])
        name = re.sub(r'(.*)_label', '\\1_input', name)
        temp = int(read_file(name)) // 1000
        db[processor_id] = temp
    return db


if len(sys.argv) < 2:
    print("usage: exec temperature-log.csv")
    sys.exit(1)
fd = open(sys.argv[1], "w")

signal.signal(signal.SIGINT, sigint_handler)
processor_core_map = get_processor_core_id_mapping()
temps = read_temps(processor_core_map)
keys = sorted(temps.keys())
fd.write(f'time;{";".join([str(x) for x in keys])}\n')

while True:
    delta_time = difftime()
    temps = read_temps(processor_core_map)
    buf = f"{delta_time:.4f}"
    for key, value in sorted(temps.items()):
        buf += f";{value}"
    fd.write(buf + "\n")
    time.sleep(1)

