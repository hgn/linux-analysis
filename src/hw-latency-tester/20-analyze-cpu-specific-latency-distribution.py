#!/usr/bin/env python3

import re
import matplotlib.pyplot as plt
from collections import defaultdict

def parse_hwlat_results(file_path):
    results = defaultdict(list)
    with open(file_path, 'r') as f:
        for line in f:
            if "inner/outer(us):" in line:
                cpu_match = re.search(r'\[(\d+)\]', line)
                if cpu_match:
                    cpu = int(cpu_match.group(1))
                    parts = line.split("inner/outer(us):")[-1].strip()
                    values, _ = parts.split("ts:")
                    inner, outer = map(int, values.split("/")[:2])
                    maxv = max(inner, outer)
                    results[cpu].extend([maxv, maxv])
    return results

def prepare_ax(ax):
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(top=False)
    ax.tick_params(left=False)
    ax.tick_params(bottom=False)
    #ax.set(yticklabels=[])
    ax.set(xticklabels=[])
    ax.tick_params(axis='y', labelcolor='0.2')
    ax.yaxis.grid(True, which='both', linestyle='--', linewidth=0.5, color='lightgray')
    ax.set_axisbelow(True)

def plot_cpu_specific_distribution(parsed_data, output_file):
    fig, ax = plt.subplots(figsize=(7, 7), dpi=300)
    prepare_ax(ax)

    cpus = sorted(parsed_data.keys())
    distributions = [parsed_data[cpu] for cpu in cpus]

    positions = range(len(cpus))
    bp = ax.boxplot(distributions, positions=positions, widths=0.4, patch_artist=True, 
                    boxprops=dict(facecolor='dimgray', color='black'), 
                    medianprops=dict(color='black', linewidth=1.5), 
                    whiskerprops=dict(color='black', linewidth=1), 
                    capprops=dict(color='black', linewidth=1))

    for box in bp['boxes']:
        box.set_facecolor('lightgray')
        box.set_alpha(1.)

    ax.set_xticks(positions)
    ax.set_xticklabels([f"CPU {cpu}" for cpu in cpus], rotation=45, ha='right')
    ax.set_xlabel("CPU", fontsize=14)
    ax.set_ylabel("Latency [us]", fontsize=14)

    fig.tight_layout()
    fig.savefig(output_file, format="pdf", transparent=True, bbox_inches="tight")
    print(f"Saved CPU-specific distribution plot to {output_file}")

def main():
    file_path = "hwlat-results.txt"
    output_file = "hwlat-cpu-latency-distribution.pdf"

    parsed_data = parse_hwlat_results(file_path)
    for cpu, data in parsed_data.items():
        print(f"CPU {cpu}: Total samples: {len(data)}")

    plot_cpu_specific_distribution(parsed_data, output_file)

if __name__ == "__main__":
    main()

