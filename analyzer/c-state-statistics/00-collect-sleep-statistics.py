#!/usr/bin/python3

import os
import sys
import json
import glob
import re


def read_file(path):
    with open(path, "r") as fd:
        return fd.read().strip()

def get_cpuidle_path_stats(path):
    return { "name" : read_file(f'{path}/name'),
             "usage" : int(read_file(f'{path}/usage')),
             "time" : int(read_file(f'{path}/time')) }

def read_c_sleeps():
    db = {}
    for path in glob.glob('/sys/devices/system/cpu/cpu*/cpuidle/state*/'):
        m = re.search(r'/sys/devices/system/cpu/cpu(\d+)/cpuidle/state(\d+)/', path)
        if not m:
            continue
        cpu_no = int(m.group(1))
        state_no = int(m.group(2))
        stats = get_cpuidle_path_stats(path)

        if cpu_no not in db:
            db[cpu_no] = dict()
        db[cpu_no][state_no] = stats
    return db

def add_sums(db):
    sum_all_cpus = {}
    for cpu, cpu_data in sorted(db.items(), key=lambda item: int(item[0])):
        for state_no, state_data in sorted(cpu_data.items(), key=lambda item: int(item[0])):
            if not state_no in sum_all_cpus:
                sum_all_cpus[state_no] = {}
                sum_all_cpus[state_no]["usage"] = 0
                sum_all_cpus[state_no]["time"] = 0
            sum_all_cpus[state_no]["name"]   = state_data["name"]
            sum_all_cpus[state_no]["usage"] += state_data["usage"]
            sum_all_cpus[state_no]["time"]  += state_data["time"]
    db["all"] = sum_all_cpus

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} <sleep-stats.json>")
    sys.exit(1)

stats = read_c_sleeps()
add_sums(stats)
with open(sys.argv[1], "w") as fd:
    json.dump(stats, fd)




