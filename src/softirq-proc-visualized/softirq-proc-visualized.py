#!/usr/bin/python3

import matplotlib.pyplot as plt
import matplotlib as mpl

# Set hatch line thickness
mpl.rcParams['hatch.linewidth'] = 0.4

DPI = 300
FIGSIZE_WIDE = (20, 8)

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
            print(f"DEBUG: CPU headers ({len(cpu_headers)}): {cpu_headers}")
            print(f"DEBUG: Values for {irq_type} ({len(values)}): {values}")
            raise ValueError(f"Mismatch between CPU count and values for {irq_type}")
        data[irq_type] = values
    return cpu_headers, data

def plot_softirq_grouped_by_cpu(cpu_headers, data, output_file="softirq-proc-visualized.pdf"):
    irq_types = list(data.keys())
    colors = ['0.2', '0.4', '0.6', '0.0']  # Three dark grayscale colors and black
    hatches = ['//', '\\\\', '||', '--', '++', 'xx', 'oo', 'OO', '..', '**']
    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE, dpi=DPI)
    bar_width = 0.85
    bottom = [0] * len(cpu_headers)
    for i, irq_type in enumerate(irq_types):
        values = [data[irq_type][j] for j in range(len(cpu_headers))]
        color = colors[i % len(colors)]
        hatch = hatches[i % len(hatches)]
        ax.bar(cpu_headers, values, width=bar_width, label=irq_type, bottom=bottom, 
               color=color, edgecolor='white', hatch=hatch, linewidth=0.0)
        bottom = [b + v for b, v in zip(bottom, values)]
    
    ax.set_ylabel("Interrupt Events")
    #ax.set_xlabel("CPU")
    ax.legend(title="SoftIRQ Types", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.set_xticks(range(len(cpu_headers)))
    ax.set_xticklabels(cpu_headers, rotation=45, ha="right")
    ax.ticklabel_format(axis="y", style="plain")
    ax.yaxis.grid(True, linestyle="--", alpha=0.7)
    ax.set_axisbelow(True)
    ax.spines.top.set_visible(False)
    ax.spines.right.set_visible(False)
    fig.tight_layout()
    plt.savefig(output_file, format="pdf", dpi=DPI, bbox_inches="tight")
    print(f"Chart saved to {output_file}")

def main():
    cpu_headers, data = parse_softirq()
    plot_softirq_grouped_by_cpu(cpu_headers, data)

if __name__ == "__main__":
    main()

