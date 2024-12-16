#!/usr/bin/env python3

import os
import time
import subprocess
import sys

TARGET_SIZE = 5_000_000_000
TARGET_SIZE = 5_000_000_0
CHUNK_SIZE = 1

EVENTS = [
    "block:*",
    "nvme:*",
    "ext4:*",
    "jbd2:*",
    "filelock:*",
    "filemap:*",
    "fs_dax:*",
    "iomap:*",
   # "page-faults",
    "iommu:*",
    "libata:*",
    "thp:*",
    "vmscan:*",
    "wbt:*",
    "writeback:*",
   # "syscalls:sys_enter_openat",
   # "syscalls:sys_exit_openat",
   # "syscalls:sys_enter_read",
   # "syscalls:sys_exit_read",
]


def build_perf_cmd(perf_output):
    perf_cmd = [
        "sudo", "taskset", "-c", "0",  # Ensure the task runs on CPU core 0
        "perf", "record",
        "-m", "16384",
        "-g",
        "-C", "5",
        "-o", perf_output
    ]

    for event in EVENTS:
        perf_cmd.extend(["-e", f'"{event}"', "--exclude-perf"])
    
    return perf_cmd



def read_files(file_list, perf_record=False, perf_output=None, break_after_first_chunk=False):
    total_read = 0
    perf_proc = None
    if perf_record and perf_output is not None:
        perf_cmd = build_perf_cmd(perf_output)
        print(f"execute: {" ".join(perf_cmd)}")
        perf_proc = subprocess.Popen(perf_cmd)
 
    # provide time that perf is started in front,
    # stupid, but simple for now. Required for small file sets
    time.sleep(1)
    for f in file_list:
        try:
            with open(f, 'rb') as fd:
                if CHUNK_SIZE is None:
                    data = fd.read()
                    total_read += len(data)
                else:
                    while True:
                        data = fd.read(CHUNK_SIZE)
                        if not data:
                            break
                        total_read += len(data)
                        if break_after_first_chunk:
                            break
        except:
            pass

    if perf_proc is not None:
        perf_proc.terminate()
        perf_proc.wait()

    return total_read

def find_and_read_initial_files(home_path, target_size):
    selected_files = []
    total_read = 0
    for root, dirs, files in os.walk(home_path):
        for file in files:
            if total_read >= target_size:
                break
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'rb') as fd:
                        file_bytes = 0
                        if CHUNK_SIZE is None:
                            data = fd.read()
                            file_bytes = len(data)
                            total_read += file_bytes
                        else:
                            while True:
                                data = fd.read(CHUNK_SIZE)
                                if not data:
                                    break
                                file_bytes += len(data)
                                total_read += len(data)
                                if total_read >= target_size:
                                    break
                        if file_bytes > 0:
                            selected_files.append(file_path)
                except:
                    pass
        if total_read >= target_size:
            break
    return selected_files, total_read

def drop_caches():
    cmd = ["sudo", "sh", "-c", "echo 3 > /proc/sys/vm/drop_caches"]
    subprocess.run(cmd, check=True)

def write_trace_marker_with_sudo(message):
    trace_marker_path = "/sys/kernel/debug/tracing/trace_marker"
    try:
        command = f'echo "{message}" | sudo tee {trace_marker_path}'
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to write marker: {e}")

def main():
    os.sched_setaffinity(0, {5})
    home_path = os.environ.get("HOME", "/home")
    selected_files, total_read = find_and_read_initial_files(home_path, TARGET_SIZE)
    if not selected_files:
        print("No files found.")
        sys.exit(1)

    num_files = len(selected_files)
    mb_processed = total_read / (1024 * 1024)
    print(f"Files Working Set: {num_files} files, total read data: {mb_processed:.2f} MB")
    print("Now drop caches ...")
    drop_caches()
    time.sleep(.5)
    write_trace_marker_with_sudo("begin FS COLD measurement")

    print("Start cold read run ...")
    start_cold = time.time()
    cold_bytes = read_files(selected_files, perf_record=True, perf_output="perf-cold.data", break_after_first_chunk=True)
    end_cold = time.time()
    cold_duration = end_cold - start_cold

    # re-pre-warm
    read_files(selected_files)

    print("Start warm read run ...")
    start_warm = time.time()
    warm_bytes = read_files(selected_files, perf_record=True, perf_output="perf-warm.data", break_after_first_chunk=True)
    end_warm = time.time()
    warm_duration = end_warm - start_warm

    diff_seconds = (cold_duration - warm_duration)
    diff_percent = (diff_seconds / cold_duration) * 100 if cold_duration != 0 else 0


    print(f"Time for Cold-Read: {cold_duration:.4f} s")
    print(f"Time for Warm-Read: {warm_duration:.4f} s")
    print(f"Difference: {diff_seconds:.4f} s ({diff_percent:.2f}%)")

if __name__ == "__main__":
    main()

