#!/usr/bin/python3

import os
import subprocess

workload = "sleep 10"

def get_perf_freq_samples(workload="sleep 20"):
    cmd = f"sudo perf record -o perf.data -a -e power:cpu_frequency -- {workload}"
    print(f"{os.path.basename(__file__)} will execute \"{cmd}\" now")
    subprocess.run(cmd, shell=True, check=True)
    cmd = f"sudo chown {os.getuid()}:{os.getgid()} perf.data"
    subprocess.run(cmd, shell=True, check=True)

get_perf_freq_samples(workload=workload)












