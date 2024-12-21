#!/usr/bin/env python3

import os
import time
import sys

def write_to_tracefs(file, content):
    with open(file, 'w') as f:
        f.write(content)

def read_from_tracefs(file):
    with open(file, 'r') as f:
        return f.read().strip()

def set_hwlat_tracer():
    write_to_tracefs("/sys/kernel/tracing/current_tracer", "hwlat")

def clear_tracer():
    write_to_tracefs("/sys/kernel/tracing/current_tracer", "nop")

def set_tracing_threshold(value):
    write_to_tracefs("/sys/kernel/tracing/tracing_thresh", str(value))

def get_tracing_threshold():
    return read_from_tracefs("/sys/kernel/tracing/tracing_thresh")

def read_hwlat_results():
    with open("/sys/kernel/tracing/trace", 'r') as f:
        return f.read()

def save_results_to_file(output_file, data):
    with open(output_file, 'w') as f:
        f.write(data)

def main():
    output_file = "hwlat-results.txt"
    measurement_duration = 960 * 2

    sys.stderr.write(f"Script started. Recording for {measurement_duration} seconds.\n")

    original_threshold = get_tracing_threshold()
    thresh_us = 10
    set_tracing_threshold(thresh_us)
    sys.stderr.write(f"Set tracing threshold to {thresh_us} us\n")

    set_hwlat_tracer()

    time.sleep(measurement_duration)

    save_results_to_file(output_file, read_hwlat_results())
    sys.stderr.write(f"Results written to {output_file}.\n")

    clear_tracer()
    sys.stderr.write("Tracer cleared.\n")

if __name__ == "__main__":
    main()

