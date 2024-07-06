#!/usr/bin/env python3

import re
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker

DPI = 300
FIGSIZE_WIDE = (17, 7)

plt.rcParams.update({'font.size': 14})

# Function to read data from the given file
def read_data(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) != 6:
                continue
            process_name = parts[0]
            tid = parts[1]
            cpu = parts[2].strip('[]')
            size = int(parts[3])
            duration = float(parts[4]) / 1000  # Convert to milliseconds
            address = parts[5]
            data.append((process_name, tid, cpu, size, duration, address))
    return data

# Function to plot the box plot
def plot_box(data):
    df = pd.DataFrame(data, columns=['process_name', 'tid', 'cpu', 'size', 'duration', 'address'])
    
    # Limit to the first 20 unique process names
    unique_processes = df['process_name'].unique()[:20]
    df = df[df['process_name'].isin(unique_processes)]
    
    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.spines.bottom.set_visible(False)
    ax.tick_params(top=False)
    ax.tick_params(left=False)
    ax.tick_params(bottom=False)

    ax.set_axisbelow(True)
    
    boxprops = dict(color='black', facecolor='lightgrey')
    whiskerprops = dict(color='black')
    capprops = dict(color='black')
    medianprops = dict(color='black')
    parts = df.boxplot(column='duration', by='process_name', ax=ax,
                       patch_artist=True, vert=False, grid=False,
                       boxprops=boxprops, whiskerprops=whiskerprops,
                       capprops=capprops, medianprops=medianprops)

    ax.yaxis.grid(False)
    ax.xaxis.grid(True, which='major', linestyle='--', linewidth='0.7', color='grey')
    ax.xaxis.grid(True, which='minor', linestyle='dotted', linewidth='0.1', color='#dddddd')

    ax.set_xscale('log')
    
    # Set the x-axis to use float tick formatting with 0.1 precision
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.1f}'))

    ax.set_ylabel('Process Name')
    ax.set_xlabel('Duration [milliseconds]')
    ax.set_title("")
    ax.get_figure().suptitle('')
    
    plt.tight_layout()
    plt.savefig('malloc-free-correlator.pdf', dpi=DPI)
    print("Saved malloc-free-correlator.pdf")

# Main function to execute the script
def main():
    filename = 'malloc-free-correlator.txt'
    data = read_data(filename)
    if not data:
        print("No data found.")
        return
    
    plot_box(data)

if __name__ == '__main__':
    main()

