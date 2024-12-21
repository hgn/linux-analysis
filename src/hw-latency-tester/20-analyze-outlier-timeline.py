#!/usr/bin/env python3

import re
import matplotlib.pyplot as plt

def parse_hwlat_results(file_path):
    results = []
    min_timestamp = None
    with open(file_path, 'r') as f:
        for line in f:
            if "inner/outer(us):" in line:
                parts = line.split("inner/outer(us):")[-1].strip()
                values, timestamp = parts.split("ts:")
                inner, outer = map(int, values.split("/")[:2])
                timestamp = float(timestamp.split()[0])
                if min_timestamp is None:
                    min_timestamp = timestamp
                normalized_timestamp = timestamp - min_timestamp
                results.append((normalized_timestamp, max(inner, outer)))
    return results

def prepare_ax(ax):
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(top=False)
    ax.tick_params(left=False)
    ax.tick_params(bottom=False)
    ax.tick_params(axis='y', labelcolor='0.2')
    ax.yaxis.grid(True, which='both', linestyle='--', linewidth=0.5, color='lightgray')
    ax.set_axisbelow(True)

def plot_scatter(parsed_data, output_file):
    timestamps = [data[0] for data in parsed_data]
    inner_values = [data[1] for data in parsed_data]

    fig, ax = plt.subplots(figsize=(7, 7), dpi=300)
    prepare_ax(ax)

    ax.scatter(timestamps, inner_values, label="Max Latency of Outer/Inner [us]",
               alpha=0.7, edgecolor="black", color="dimgray")
    #ax.scatter(timestamps, inner_values, label="Inner Latency (us)", alpha=1., edgecolor="black", color="black")

    ax.set_xlabel("Time [s]", fontsize=14)
    ax.set_ylabel("Latency [us]", fontsize=14)
    ax.legend()

    fig.tight_layout()
    fig.savefig(output_file, format="pdf", transparent=False, bbox_inches="tight")
    print(f"Saved scatter plot to {output_file}")

def main():
    file_path = "hwlat-results.txt"
    output_file = "hwlat-outlier-timeline.pdf"

    parsed_data = parse_hwlat_results(file_path)
    for timestamp, maxv in parsed_data:
        print(f"Timestamp: {timestamp}, max(Inner/Outer) {maxv} us")

    plot_scatter(parsed_data, output_file)

if __name__ == "__main__":
    main()

