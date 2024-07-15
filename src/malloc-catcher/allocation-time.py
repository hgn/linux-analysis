#!/usr/bin/env python3

import re
import subprocess
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
from collections import defaultdict

DPI = 300
FIGSIZE_WIDE = (15, 7)
INTERVAL = 10

plt.rcParams.update({'font.size': 14})

# Define line styles
LINE_STYLES = ['-', '--', '-.', ':', (0, (1, 1)), (0, (5, 1)), (0, (3, 5, 1, 5)), (0, (3, 1, 1, 1))]

# Function to execute 'perf script' and get the output lines
def get_perf_script_output():
    try:
        result = subprocess.run(['perf', 'script'], capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error executing perf script: {e}")
        return []

# Function to parse the perf script output and aggregate allocations per process per 10 seconds
def parse_allocations(lines):
    allocations = defaultdict(lambda: defaultdict(int))
    pattern = re.compile(r'^\s*(\S+)\s+\d+\s+\[\d+\]\s+(\d+\.\d+): probe_libc:malloc: \(\S+\) size=(\d+)')
    
    for line in lines:
        match = pattern.match(line)
        if match:
            process_name = match.group(1)
            timestamp = float(match.group(2))
            size = int(match.group(3))
            interval = int(timestamp // INTERVAL)
            allocations[process_name][interval] += size
    
    for process_name in allocations:
        for interval in allocations[process_name]:
            allocations[process_name][interval] /= (1024)
    
    return allocations

# Function to plot the allocations
def plot_allocations(allocations):
    # Calculate total allocations per process
    total_allocations = {process_name: sum(sizes.values()) for process_name, sizes in allocations.items()}
    
    # Sort by total allocations and select the top 10 processes
    top_processes = sorted(total_allocations, key=total_allocations.get, reverse=True)[:10]
    
    # Filter the allocations to include only the top 10 processes
    filtered_allocations = {process: allocations[process] for process in top_processes}
    
    df = pd.DataFrame(filtered_allocations).fillna(0)
    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.spines.left.set_visible(False)
    ax.tick_params(top=False)
    ax.tick_params(left=False)
    ax.tick_params(bottom=False)
    ax.yaxis.grid(True, which='major', linestyle='--', linewidth='0.5', color='grey')
    ax.set_axisbelow(True)  # Ensure grid lines are in the background
    
    for idx, process_name in enumerate(df.columns):
        ax.plot(df.index * INTERVAL, df[process_name], label=process_name, linestyle=LINE_STYLES[idx % len(LINE_STYLES)], color='black')
    
    ax.set_xlabel('Time [seconds]')
    ax.set_ylabel('Memory Allocations per 10 Seconds [KiB]')
    
    # Set the y-axis to use integer tick formatting
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.0f}'))
    
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('allocations-time.pdf', dpi=DPI)
    print("File saved as allocations-time.pdf")

# Main function to execute the script
def main():
    lines = get_perf_script_output()
    if not lines:
        print("No data from perf script.")
        return
    
    allocations = parse_allocations(lines)
    if not allocations:
        print("No malloc allocations found.")
        return
    
    plot_allocations(allocations)

if __name__ == '__main__':
    main()

