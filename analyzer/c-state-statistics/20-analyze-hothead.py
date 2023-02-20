#!/usr/bin/python3

import sys
import matplotlib.pyplot as plt
import matplotlib
import json

plt.style.use('grayscale')
DPI=300
FIGSIZE_WIDE = (12,7)

def prepare_ax(ax):
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.spines.bottom.set_visible(False)
    ax.spines.left.set_visible(False)
    ax.tick_params(top=False)
    ax.tick_params(left=False)
    ax.tick_params(bottom=False)
    ax.set(yticklabels=[])
    ax.set(xticklabels=[])
    ax.tick_params(left=False)

def load_json_file(filename):
    with open(filename) as fd:
        return json.load(fd)

def transform_data(db):
    times = []
    usages = []
    lables = []
    for state, state_data in db["all"].items():
        lables.append(state_data["name"])
        times.append(state_data["time"])
        usages.append(state_data["usage"])
    return lables, times, usages



db = load_json_file("sleep-stats.json")

labels, times, usages = transform_data(db)

fig, ax = plt.subplots()
ax.pie(usages, labels=labels, autopct='%1.1f%%')

image_filename = sys.argv[1] if len(sys.argv) > 1 else "graph.pdf"
fig.savefig(image_filename, dpi=DPI, bbox_inches='tight')
print(f"save file as {image_filename}")
