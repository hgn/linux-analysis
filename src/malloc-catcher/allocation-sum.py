#!/usr/bin/env python3

import re
import subprocess
import matplotlib.pyplot as plt

DPI = 300
FIGSIZE_WIDE = (15, 7)

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
    allocations = {}
    pattern = re.compile(r'^\s*(\S+)\s+\d+\s+\[\d+\]\s+\d+\.\d+: probe_libc:malloc: \(\S+\) size=(\d+)')
    
    for line in lines:
        match = pattern.match(line)
        if match:
            process_name = match.group(1)
            size = int(match.group(2))
            if process_name in allocations:
                allocations[process_name] += size
            else:
                allocations[process_name] = size
    
    # Convert allocations to MiB
    for process_name in allocations:
        allocations[process_name] /= (1024 * 1024)
    
    return allocations

# Function to plot the allocations
def plot_allocations(allocations):
    # Sort allocations by size and select the top 10
    sorted_allocations = sorted(allocations.items(), key=lambda item: item[1], reverse=True)[:10]
    
    processes = [item[0] for item in sorted_allocations]
    sizes = [item[1] for item in sorted_allocations]
    
    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.spines.left.set_visible(False)
    ax.tick_params(top=False)
    ax.tick_params(left=False)
    ax.tick_params(bottom=False)
    ax.yaxis.grid(True, which='major', linestyle='--', linewidth='0.5', color='grey')
    ax.set_axisbelow(True)  # Ensure grid lines are in the background

    # Use grayscale color
    ax.bar(processes, sizes, color='gray')
    
    ax.set_xlabel('Processes')
    ax.set_ylabel('Total Memory Allocated [MiB]')
    #ax.set_title('Memory Allocations per Process')
    ax.set_xticks(processes)
    ax.set_xticklabels(processes, rotation=45, ha='right')
    
    plt.tight_layout()
    fig.savefig('allocations-sum.pdf', dpi=DPI, bbox_inches='tight')
    print("File saved as allocations-sum.pdf")

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

