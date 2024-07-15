#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np

DPI = 300
FIGSIZE_WIDE = (15, 7)

def prepare_ax(ax):
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    #ax.spines.bottom.set_visible(False)
    #ax.spines.left.set_visible(False)
    ax.tick_params(top=False)
    ax.tick_params(left=False)
    ax.tick_params(bottom=False)
    #ax.set(yticklabels=[])
    #ax.set(xticklabels=[])
    ax.tick_params(left=False)
    ax.yaxis.grid(True, which='major', linestyle='--', linewidth='0.5', color='grey')
    ax.set_axisbelow(True)  # Ensure grid lines are in the background

def parse_meminfo(filename, fields):
    data = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if parts[0].rstrip(':') in fields:
                data[parts[0].rstrip(':')] = int(parts[1]) / (1024 * 1024)  # Convert kB to GiB
    return data

def add_labels(bars, ax):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

# Files to read
before_file = 'meminfo-before-cat.txt'
after_file = 'meminfo-after-cat-100-mebibytes.txt'

# Fields to extract
fields = ['MemTotal', 'MemFree', 'MemAvailable', 'Cached', 'Inactive(file)', 'Active(file)']

# Parse the files
before_data = parse_meminfo(before_file, fields)
after_data = parse_meminfo(after_file, fields)

# Extract values in the order of fields
before_values = [before_data[field] for field in fields]
after_values = [after_data[field] for field in fields]

# Create the grouped bar chart
fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)

bar_width = 0.35
index = np.arange(len(fields))

colors = ['#404040', '#808080']

bars1 = ax.bar(index, before_values, bar_width, label='Before Cat Paging Caching', color=colors[0])
bars2 = ax.bar(index + bar_width, after_values, bar_width, label='After Cat Paging Caching', color=colors[1])

# Labels and title
ax.set_xlabel('Memory Metrics')
ax.set_ylabel('Values (GiB)')
#ax.set_title('Memory Metrics Before and After')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(fields, rotation=45, ha="right")
ax.legend()

add_labels(bars1, ax)
add_labels(bars2, ax)

prepare_ax(ax)

plt.tight_layout()

fig.savefig('page-cacher.pdf', dpi=DPI, bbox_inches='tight')

print("Save file page-cacher.pdf")

