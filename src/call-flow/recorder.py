#!/usr/bin/env python3

import subprocess
import signal
import os

CORE = 10  # Core number as an integer

def start_background_perf():
    """
    Starts the background perf recording process.
    Returns the subprocess.Popen object.
    """
    perf_command = [
        'perf', 'record', '-D', '100',
        '-o', 'perf-sched-switch.data',
        '-C', str(CORE),  # Convert CORE to string
        '-e', 'sched:sched_switch'
    ]
    return subprocess.Popen(perf_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def run_workload():
    """
    Runs the workload perf command, blocking until completion.
    """
    perf_command = [
        'perf', 'record', '-D', '100',  # Convert CORE to string
        '-g', '--call-graph', 'dwarf',
        '-e', 'syscalls:sys_enter_*,syscalls:sys_exit_*,cpu_core/cycles/u',
        '--', 'taskset', '-c', str(CORE), './call-flow-example'
    ]
    subprocess.run(perf_command, check=True)

def main():
    # Start the background perf process
    background_perf = start_background_perf()
    print(f"Started background perf with PID {background_perf.pid}")

    try:
        # Run the workload
        print("start workload now")
        run_workload()
    finally:
        print(f"Terminating background perf with PID {background_perf.pid}")
        os.kill(background_perf.pid, signal.SIGINT)
        
        # Wait for the process to terminate cleanly
        background_perf.wait()
        print("Background perf terminated.")

if __name__ == "__main__":
    main()

