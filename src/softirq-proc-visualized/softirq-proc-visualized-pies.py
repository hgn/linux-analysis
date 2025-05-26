#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib as mpl
import math

DPI = 300
FIGSIZE = (24, 12)

# Druckfreundliche dunkle Graustufen
GRAYSCALE_COLORS = [
    "#bbbbbb", "#aaaaaa", "#999999", "#888888", "#777777",
    "#666666", "#555555", "#444444", "#333333", "#222222"
]

def parse_softirq(file_path: str = "/proc/softirqs"):
    with open(file_path, "r") as file:
        lines = file.readlines()
    cpu_headers = lines[0].split()
    data = {}
    for line in lines[1:]:
        parts = line.split(":")
        irq_type = parts[0].strip()
        values = list(map(int, parts[1].split()))
        if len(values) != len(cpu_headers):
            raise ValueError(f"Mismatch between CPU count and values for {irq_type}")
        data[irq_type] = values
    return cpu_headers[:32], {k: v[:32] for k, v in data.items()}  # Max 32 CPUs

def plot_softirq_piecharts(cpu_headers, data, output_file="softirq-proc-visualized-pies.pdf"):
    irq_types = list(data.keys())
    num_cpus = len(cpu_headers)

    cols = 8
    rows = math.ceil(num_cpus / cols)

    fig, axes = plt.subplots(rows, cols, figsize=FIGSIZE, dpi=DPI)
    axes = axes.flatten()

    for i, cpu in enumerate(cpu_headers):
        ax = axes[i]
        values_raw = [data[irq_type][i] for irq_type in irq_types]
        total = sum(values_raw)
        if total == 0:
            ax.axis('off')
            continue

        # Filter: nur Werte >= 1% anzeigen
        values = []
        labels = []
        for j, count in enumerate(values_raw):
            if count / total >= 0.01:
                values.append(count)
                labels.append(irq_types[j])

        if not values:
            ax.axis('off')
            continue

        colors = GRAYSCALE_COLORS[:len(values)]
        ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%',
               startangle=90, textprops={'fontsize': 8})
        ax.set_title(cpu, fontsize=10)

    # Entferne leere Subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    #fig.suptitle("SoftIRQ-Verteilung (≥1 %) über 32 CPUs", fontsize=14)
    fig.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.savefig(output_file, format="pdf", bbox_inches="tight")
    print(f"Filtered pie charts saved to {output_file}")

def main():
    cpu_headers, data = parse_softirq()
    plot_softirq_piecharts(cpu_headers, data)

if __name__ == "__main__":
    main()

