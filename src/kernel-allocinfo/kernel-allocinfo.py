#!/usr/bin/env python3

import subprocess
import itertools
import time
import sys
from typing import Dict, List
import pandas as pd
import matplotlib.pyplot as plt

# Constants
NUM_ITERATIONS = 10
SLEEP_INTERVAL = 1

plt.style.use('grayscale')
plt.rcParams.update({'font.size': 13})

DPI = 300
FIGSIZE = (14, 5)
LINEWIDTH = 1.0
LINESTYLES = ['-', '--', ':', '-.']

TIMEREF = time.time()


def read_allocinfo() -> Dict[str, int]:
    """
    Reads `/proc/allocinfo` via `sudo` and extracts key-value pairs.
    The key format is `path:func` and the value is the first column (size).
    """
    try:
        # Use sudo to read `/proc/allocinfo`
        result = subprocess.run(
            ["sudo", "cat", "/proc/allocinfo"],
            capture_output=True,
            text=True,
            check=True
        )
        allocinfo_lines = result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error reading /proc/allocinfo: {e}")
        return {}

    # Parse the lines to extract size and keys
    data = {}
    for line in allocinfo_lines:
        # Skip comment lines or lines that don't start with a number
        if line.startswith("#") or not line.split()[0].isdigit():
            continue
        
        parts = line.split()
        if len(parts) >= 4:  # Ensure the line has enough elements
            try:
                size = float(parts[0]) / 1024
                if not parts[2].startswith("net/"):
                    continue
                path_func = f"{parts[2].split(":")[0]}:{parts[-1].split(":")[1]}()"
                if path_func not in data:
                    data[path_func] = 0
                data[path_func] += size
                #path_func = f"{parts[2].split(":")[0].split("/")[0]}" 
                #if path_func not in data:
                #    data[path_func] = 0
                #data[path_func] += size
            except (ValueError, IndexError) as e:
                # Handle any unexpected format issues gracefully
                print(f"Skipping malformed line: {line}")
    return data

def collect_data(num_iterations: int, sleep_interval: int) -> pd.DataFrame:
    """
    Collects `/proc/allocinfo` data over multiple iterations.
    Stores the data in a pandas DataFrame.
    """
    time_series_data = []

    for i in range(num_iterations):
        print(f"Iteration {i + 1}/{num_iterations}")
        allocinfo = read_allocinfo()
        timestamp = time.time()
        allocinfo["timestamp"] = timestamp - TIMEREF
        time_series_data.append(allocinfo)
        time.sleep(sleep_interval)

    # Convert the time series data into a pandas DataFrame
    df = pd.DataFrame(time_series_data)
    df.set_index("timestamp", inplace=True)
    return df


def visualize_data(df: pd.DataFrame, output_filepath: str = "allocations_plot.pdf"):
    df_filled = df.fillna(0)  # Fill NaN with 0 for proper visualization
    last_row = df.iloc[-1].dropna()  # Use only non-NaN values for sorting
    sorted_keys = last_row.sort_values(ascending=False).index  # Sort by the last row's values
    top_keys = sorted_keys[:5]

    # Initialize figure and axis
    fig, ax1 = plt.subplots(figsize=FIGSIZE)

    # Style adjustments
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.set_axisbelow(True)
    ax1.grid(color='grey', axis='y', linestyle=':', linewidth=0.8)

    linestyle_cycler = itertools.cycle(LINESTYLES)

    for key in top_keys:
        ax1.plot(
            df.index,
            df_filled[key],
            label=key,
            linewidth=LINEWIDTH,
            color="black",
            linestyle=next(linestyle_cycler),
            alpha=1.0
        )

    ax1.set_xlabel('Timestamp')
    ax1.set_ylabel('Allocation Size [KiB]', color='0.')
    #ax1.set_yscale('log')  # Logarithmic scale for y-axis
    #ax1.tick_params(axis='y', labelcolor='0.')

    ax1.legend(
        loc='upper left',
        bbox_to_anchor=(1, 1),
        fontsize=10,
        ncol=1,
        frameon=False
    )

    fig.tight_layout(pad=0)

    fig.savefig(output_filepath, dpi=DPI, bbox_inches='tight')
    print(f"Plot saved as {output_filepath}")


def main():
    print("Starting to collect data from /proc/allocinfo...")
    df = collect_data(NUM_ITERATIONS, SLEEP_INTERVAL)
    print("Data collection complete. Visualizing...")
    visualize_data(df)

if __name__ == "__main__":
    main()

