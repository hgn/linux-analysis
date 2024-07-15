#!/usr/bin/env python3

import re
import subprocess
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import ScalarFormatter
from collections import defaultdict

DPI = 300
FIGSIZE_WIDE = (18, 7)

plt.rcParams.update({'font.size': 14})

# Function to execute 'perf script' and get the output lines
def get_perf_script_output():
    try:
        result = subprocess.run(['perf', 'script'], capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error executing perf script: {e}")
        return []

# Function to parse the perf script output and aggregate allocations per process
def parse_allocations(lines):
    allocations = defaultdict(list)
    pattern = re.compile(r'^\s*(\S+)\s+\d+\s+\[\d+\]\s+(\d+\.\d+): probe_libc:malloc: \(\S+\) size=(\d+)')
    
    for line in lines:
        match = pattern.match(line)
        if match:
            process_name = match.group(1)
            size = int(match.group(3))
            allocations[process_name].append(size)
    
    return allocations

# Function to plot the allocations
def plot_allocations(allocations):
    # Calculate total allocations per process
    total_allocations = {process_name: sum(sizes) for process_name, sizes in allocations.items()}
    
    # Sort by total allocations and select the top 10 processes
    top_processes = sorted(total_allocations, key=total_allocations.get, reverse=True)[:10]
    
    # Filter the allocations to include only the top 10 processes
    filtered_allocations = {process: allocations[process] for process in top_processes}
    
    # Sort filtered allocations for plotting
    sorted_filtered_allocations = dict(sorted(filtered_allocations.items(), key=lambda item: total_allocations[item[0]], reverse=True))
    
    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    #ax.spines.bottom.set_visible(False)
    ax.spines.left.set_visible(False)
    ax.tick_params(top=False)
    ax.tick_params(left=False)
    ax.tick_params(bottom=False)
    #ax.set(yticklabels=[])
    #ax.set(xticklabels=[])
    ax.tick_params(left=False)
    ax.xaxis.grid(True, which='major', linestyle='--', linewidth='0.7', color='grey')
    ax.xaxis.grid(True, which='minor', linestyle='dotted', linewidth='0.2', color='grey')
    ax.set_axisbelow(True)  # Ensure grid lines are in the background
    
    # Create the violin plot
    parts = ax.violinplot(sorted_filtered_allocations.values(), vert=False, showmeans=True, showmedians=True, showextrema=True)
    
    # Set the y-tick labels to process names
    ax.set_yticks(range(1, len(sorted_filtered_allocations) + 1))
    ax.set_yticklabels(sorted_filtered_allocations.keys())
    
    # Labeling the axes
    ax.set_xlabel('Memory Allocated [bytes]')
    ax.set_xscale('log')
    #ax.set_title('Distribution of Memory Allocations Per Process')

    # Set integer formatting for x-axis
    ax.xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    
    # Customize the plot appearance
    for pc in parts['bodies']:
        pc.set_facecolor('gray')
        pc.set_edgecolor('black')
        pc.set_alpha(0.7)

    for partname in ('cbars', 'cmins', 'cmaxes', 'cmeans', 'cmedians'):
        vp = parts[partname]
        vp.set_edgecolor('black')
        vp.set_linewidth(1)

    #for i, (process, sizes) in enumerate(sorted_filtered_allocations.items(), start=1):
    #    mean = np.mean(sizes)
    #    median = np.median(sizes)
    #    ax.scatter(mean, i, color='black', marker='o')
    #    ax.scatter(median, i, color='black', marker='x')
    #    ax.hlines(i, min(sizes), max(sizes), color='black', linestyle='--', alpha=0.3)
    #
    ## Add legend for mean and median
    #handles, labels = ax.get_legend_handles_labels()
    #unique_labels = dict(zip(labels, handles))
    #ax.legend(unique_labels.values(), unique_labels.keys())
    
    plt.tight_layout()
    fig.savefig('allocations-spread.pdf', dpi=DPI, bbox_inches='tight')
    print("Save file allocations-spread.pdf")

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

