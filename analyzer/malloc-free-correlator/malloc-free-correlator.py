#!/usr/bin/env python3

import re
import subprocess

# Function to execute 'perf script' and get the output lines
def get_perf_script_output():
    try:
        result = subprocess.run(['perf', 'script'], capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error executing perf script: {e}")
        return []

# Regular expressions to match the events
malloc_pattern = re.compile(r'probe_libc:malloc: .* size=(\d+)')
malloc_ret_pattern = re.compile(r'probe_libc:malloc_ret__return: .* arg1=(0x[0-9a-f]+)')
free_pattern = re.compile(r'probe_libc:free: .* mem=(\d+)')

# Regular expression to extract process name, tid, cpu, and timestamp
line_pattern = re.compile(r'^(.*?)\s+(\d+)\s+\[(\d+)\]\s+(\d+\.\d+):.*')

# Dictionaries to store malloc and free events
mallocs = {}
frees = []

# Function to convert unsigned 64-bit to signed 64-bit if needed
def convert_to_signed_64(decimal_number):
    if decimal_number >= 2**63:
        decimal_number -= 2**64
    return decimal_number

# Parse the perf script output
def parse_perf_script(lines):
    for line in lines:
        line_match = line_pattern.match(line)
        if not line_match:
            continue

        # Extract the process name, tid, cpu, and timestamp
        process_name = line_match.group(1).strip()
        tid = line_match.group(2).strip()
        cpu = line_match.group(3).strip()
        timestamp = float(line_match.group(4).strip())

        malloc_match = malloc_pattern.search(line)
        malloc_ret_match = malloc_ret_pattern.search(line)
        free_match = free_pattern.search(line)
        
        if malloc_match:
            size = int(malloc_match.group(1))
            # Initialize the malloc entry
            if tid not in mallocs:
                mallocs[tid] = []
            mallocs[tid].append({'size': size, 'addr': None, 'malloc_time': None, 'process_name': process_name, 'cpu': cpu})
        
        if malloc_ret_match:
            addr = int(malloc_ret_match.group(1), 16)
            addr = convert_to_signed_64(addr)
            # Update the most recent malloc entry with the returned address and time
            if tid in mallocs and mallocs[tid][-1]['addr'] is None:
                mallocs[tid][-1]['addr'] = addr
                mallocs[tid][-1]['malloc_time'] = timestamp
        
        if free_match:
            addr = int(free_match.group(1))
            addr = convert_to_signed_64(addr)
            # Add the free event
            frees.append((tid, addr, timestamp, process_name, cpu))

# Correlate malloc and free events
def correlate_events():
    matched = set()
    for tid, addr, free_time, process_name, cpu in frees:
        if tid in mallocs:
            for entry in mallocs[tid]:
                if entry['addr'] == addr and (tid, addr) not in matched:
                    malloc_time = entry['malloc_time']
                    time_diff = (free_time - malloc_time) * 1e6  # Convert seconds to microseconds
                    if time_diff < 0:
                        continue
                    print(f"{entry['process_name']} {tid} [{cpu}] {entry['size']} {time_diff:.2f} {hex(addr)}")
                    matched.add((tid, addr))

# Main function to execute the script
def main():
    lines = get_perf_script_output()
    if not lines:
        print("No data from perf script.")
        return
    
    parse_perf_script(lines)
    correlate_events()

if __name__ == '__main__':
    main()

