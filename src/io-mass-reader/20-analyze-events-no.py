#!/usr/bin/python3

import subprocess
import matplotlib.pyplot as plt
import numpy as np

DPI = 300
FIGSIZE_WIDE = (14, 7)
MIN_EVENTS_THRESHOLD = 100

def prepare_ax(ax):
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.tick_params(top=False)
    ax.tick_params(left=False)
    ax.tick_params(bottom=False)
    ax.set(yticklabels=[])
    ax.set(xticklabels=[])
    ax.tick_params(left=False)
    ax.tick_params(axis='y', labelcolor='0.2')
    ax.yaxis.grid(True, which='both', linestyle='--', linewidth=0.5, color='lightgray')
    ax.set_axisbelow(True)

def format_number(num):
    if num >= 1_000_000:
        return f" {num / 1_000_000:.1f}G"
    elif num >= 1_000:
        return f" {num / 1_000:.1f}K"
    return str(num)

def read_events(filename):
    result = subprocess.run(["perf", "script", "-F", "event", "-i", filename], capture_output=True, text=True)
    events = result.stdout.strip().split("\n")
    event_counts = {}
    for event in events:
        if event in event_counts:
            event_counts[event] += 1
        else:
            event_counts[event] = 1
    return {event: count for event, count in event_counts.items() if count >= MIN_EVENTS_THRESHOLD}

def plot_grouped_bar_chart(data_cold, data_warm, output_file):
    all_events = {}
    for event, count in data_cold.items():
        all_events[event] = all_events.get(event, 0) + count
    for event, count in data_warm.items():
        all_events[event] = all_events.get(event, 0) + count

    sorted_events = sorted(all_events.keys(), key=lambda e: all_events[e], reverse=True)
    counts_cold = [data_cold.get(event, 0) for event in sorted_events]
    counts_warm = [data_warm.get(event, 0) for event in sorted_events]

    x = np.arange(len(sorted_events))
    width = 0.35

    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE, dpi=DPI)
    prepare_ax(ax)

    bars_cold = ax.bar(x - width / 2, counts_cold, width, label="Cold", color="#555555")
    bars_warm = ax.bar(x + width / 2, counts_warm, width, label="Warm", color="#aaaaaa")

    for bar, count in zip(bars_cold, counts_cold):
        if count > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, format_number(count), 
                    ha='center', va='bottom', fontsize=8, color="black", rotation=90)

    for bar, count in zip(bars_warm, counts_warm):
        if count > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, format_number(count), 
                    ha='center', va='bottom', fontsize=8, color="black", rotation=90)

    ax.set_xlabel("Event")
    ax.set_ylabel("Occurrences [log scale]")
    ax.set_xticks(x)
    ax.set_xticklabels(sorted_events, rotation=45, ha="right")
    ax.set_yscale('log')
    ax.legend()

    fig.tight_layout()
    fig.savefig(output_file, format='pdf', dpi=DPI, transparent=True, bbox_inches='tight')
    print(f"Saved chart to {output_file}")

def main():
    cold_file = "perf-cold.data"
    warm_file = "perf-warm.data"
    
    data_cold = read_events(cold_file)
    data_warm = read_events(warm_file)
    
    output_file = "event_comparison.pdf"
    plot_grouped_bar_chart(data_cold, data_warm, output_file)

if __name__ == "__main__":
    main()

