#!/usr/bin/python3

import os
import subprocess

def prepare_data():
    cmd = f"perf script -i perf.data -s ./prepare-perf-script-frequency.py"
    print(f"{os.path.basename(__file__)} will execute \"{cmd}\" now")
    subprocess.run(cmd, shell=True, check=True)

prepare_data()
