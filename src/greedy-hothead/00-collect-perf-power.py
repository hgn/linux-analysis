#!/usr/bin/python3

import os
import sys
import subprocess
import pathlib
import shutil
import time

KERNEL_SRC_DIR = pathlib.Path("~/src/code/linux")
KERNEL_TARGET = "allyesconfig"
TMP_BUILD_DIR = "/tmp/linux-kernel-dir"



def run_greedy_hothead():
    cmd = f"sudo nice -20 ./greedy-hothead"
    spawn(cmd)

def run_kernel_build():
    shutil.rmtree(TMP_BUILD_DIR, ignore_errors=True)
    os.mkdir(TMP_BUILD_DIR)
    cmd = f"make -C {KERNEL_SRC_DIR.expanduser()} O={TMP_BUILD_DIR} {KERNEL_TARGET}"
    spawn(cmd)
    cmd = f"make -C {KERNEL_SRC_DIR.expanduser()} O={TMP_BUILD_DIR} -j $(nproc)"
    spawn(cmd)



def bg_spawn(cmd):
    print(cmd)
    return subprocess.Popen(cmd, shell=True)

def spawn(cmd):
    print(cmd)
    subprocess.run(cmd, shell=True, check=True)

cmd = f"sudo ./cpu-temp-collector.py 2> temp-log.csv"
task1 = bg_spawn(cmd)

cmd = f"stdbuf -oL -eL sudo ./rapl-read/rapl-plot -p > power-log.csv"
task2 = bg_spawn(cmd)

cmd = f"sudo ./cpu-freq-collector.py 2> freq-log.csv"
task3 = bg_spawn(cmd)

time.sleep(5)

run_greedy_hothead()

os.sync()
task1.terminate()
task2.terminate()
task3.terminate()





