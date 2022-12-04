from __future__ import print_function

import os
import sys
import json
import datetime

sys.path.append(os.environ['PERF_EXEC_PATH'] + \
	'/scripts/python/Perf-Trace-Util/lib/Perf/Trace')

from perf_trace_context import *
from Core import *

db = {}
stats = {}

def trace_begin():
    global stats
    stats["recording-timestamp"] = datetime.datetime.now().isoformat()
    stats["freq-min"] = 9999999999
    stats["freq-max"] = 0
    stats["time-min"] = None
    stats["time-max"] = None
    stats["frequencies"] = {}
    stats["data"] = {}


def update_stats(stats, cpu, time, freq):
    time = float(time)
    if not freq in stats["frequencies"]:
        stats["frequencies"][freq] = 0
    stats["frequencies"][freq] += 1
    if cpu not in stats["data"]:
        stats["data"][cpu] = {}
        stats["data"][cpu]["cpu-id"] = cpu
        stats["data"][cpu]["cpu-long-id"] = "{:03d}".format(cpu)
    if stats["time-min"] == None:
        stats["time-min"] = time
        stats["time-max"] = time
    if time > stats["time-max"]:
        stats["time-max"] = time
    if time < stats["time-min"]:
        stats["time-min"] = time
    if freq < stats["freq-min"]:
        stats["freq-min"] = freq
    if freq > stats["freq-max"]:
        stats["freq-max"] = freq


def save_stats(stats):
    with open('meta.json', 'w') as fd:
        json.dump(stats, fd, indent=4)


def open_files(db, stats):
    files = {}
    for cpu in db.keys():
        filename = "trace-{:03d}.csv".format(cpu)
        stats["data"][cpu]["filename"] = filename
        files[cpu] = open(filename, "w")
    return files


def close_files(files):
    for fd in files.values():
        fd.close()


def trace_end():
    global stats
    files = open_files(db, stats)
    for cpu in db.keys():
        for time, new_freq in db[cpu]:
            line = "{},{}\n".format(time, new_freq)
            files[cpu].write(line)
    close_files(files)
    save_stats(stats)


def convert_time(secs, nsecs):
    return secs + float(nsecs) / 1e9


def power__cpu_frequency(event_name, context, common_cpu,
                         common_secs, common_nsecs, common_pid, common_comm,
                         common_callchain, state, cpu_id, perf_sample_dict):
        global db; global stats
        _cpu = int(cpu_id)
        if _cpu not in db:
            db[_cpu] = []
        time = convert_time(common_secs, common_nsecs)
        freq = int(state)
        db[_cpu].append([time, freq])
        update_stats(stats, _cpu, time, freq)


def trace_unhandled(event_name, context, event_fields_dict, perf_sample_dict):
    pass
