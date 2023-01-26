#!/usr/bin/python3

import os
import sys
import subprocess
import psutil
import time
import pprint

start_time = time.time()

def difftime():
    return time.time() - start_time

while True:
    delta_time = difftime()
    ret = psutil.cpu_freq(percpu=True)
    sys.stderr.write(f"{delta_time:.2f};")
    stripped = [str(int(item[0])) for item in ret]
    sys.stderr.write(f'{";".join(stripped)}\n')
    time.sleep(1)
