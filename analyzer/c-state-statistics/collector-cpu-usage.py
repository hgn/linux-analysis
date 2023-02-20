#!/usr/bin/python3

import os
import sys
import psutil
import time
import signal


def difftime():
    return time.time() - start_time

def sigint_handler(sig, frame):
    os.sync()
    fd.close()
    sys.exit(0)

def read_usage():
    return psutil.cpu_percent(interval=None, percpu=True)

if len(sys.argv) < 2:
    sys.exit(1)
fd = open(sys.argv[1], "w")
signal.signal(signal.SIGINT, sigint_handler)
header = range(len(read_usage()))
fd.write(f'time;{";".join([str(x) for x in header])}\n')

start_time = time.time()

while True:
    delta_time = difftime()
    temps = read_usage()
    buf = f'{delta_time:.4f};{";".join([str(x) for x in temps])}'
    fd.write(buf + "\n")
    time.sleep(1)
