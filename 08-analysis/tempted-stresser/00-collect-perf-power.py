#!/usr/bin/python3

import os
import sys
import time
import subprocess
import signal
import pathlib
import shutil

KERNEL_SRC_DIR = pathlib.Path("~/src/code/linux")
KERNEL_TARGET = "allyesconfig"
TMP_BUILD_DIR = "/tmp/linux-kernel-dir"

def run_kernel_build():
    shutil.rmtree(TMP_BUILD_DIR, ignore_errors=True)
    os.mkdir(TMP_BUILD_DIR)
    cmd = f"make -C {KERNEL_SRC_DIR.expanduser()} O={TMP_BUILD_DIR} {KERNEL_TARGET}"
    spawn(cmd)
    cmd = f"make -C {KERNEL_SRC_DIR.expanduser()} O={TMP_BUILD_DIR} -j $(($(nproc)))"
    spawn(cmd)

def stress():
    """ run nproc / 2 cpu hogs"""
    cmd = f"stress --cpu $(($(nproc)/2)) -t 20"
    spawn(cmd)

def bg_spawn(cmd):
    print(cmd)
    return subprocess.Popen(cmd.split(), shell=False)

def spawn(cmd):
    print(cmd)
    subprocess.run(cmd, shell=True, check=True)

cmd = f"./collector-cpu-temperature.py log-temperature.csv"
monitor_task1 = bg_spawn(cmd)

cmd = f"./collector-cpu-usage.py log-usage.csv"
monitor_task2 = bg_spawn(cmd)

#stress()
run_kernel_build()

# leave some time to catch all data 
time.sleep(1)
os.kill(monitor_task1.pid, signal.SIGINT)
os.kill(monitor_task2.pid, signal.SIGINT)
time.sleep(1)
os.kill(monitor_task1.pid, signal.SIGKILL)
os.kill(monitor_task2.pid, signal.SIGKILL)
