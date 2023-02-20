#!/usr/bin/python3

import os
import subprocess


cmd = f"perf script -s ./convert-perf-data-to-c-accumulative.py > cpu-idle.json"
print(f"{os.path.basename(__file__)} will execute \"{cmd}\" now")
subprocess.run(cmd, shell=True, check=True)













