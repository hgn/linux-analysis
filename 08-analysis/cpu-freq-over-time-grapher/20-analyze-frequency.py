#!/usr/bin/python3

import os
import sys
import json
import pathlib
import tempfile
import subprocess
import pprint
#import colour
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

plt.style.use('grayscale')
stats_path = 'meta.json'

DPI=300

def load_stats():
    with open(stats_path) as fd:
        return json.load(fd)

def df_by_file(filename):
    df = pd.read_csv(filename, names= ['time','frequency'], header=None)
    df = df.astype({'time':'float','frequency':'int'})
    df["frequency"] = df["frequency"].div(1000000)
    return df

def populate_artifal_switch(df, stats):
    times = []; frequencies = []; first = True; frequency_last = False
    for index, row in df.iterrows():
        time = row["time"] - float(stats["time-min"])
        frequency = row["frequency"]
        if not frequency_last:
            times.append(time)
            frequencies.append(frequency)
            frequency_last = frequency
            continue
        # artifical entry, short before real
        times.append(time - sys.float_info.min)
        frequencies.append(frequency_last)
        # real switching event
        times.append(time)
        frequencies.append(frequency)
        frequency_last = frequency
    # finale, tail the last entry till ever last event
    times.append(stats["time-max"] - float(stats["time-min"]))
    frequencies.append(frequency_last)
    return times, frequencies

def draw_line(ax, df, stats):
    times, frequencies =  populate_artifal_switch(df, stats)
    ax.set_ylim([stats["freq-min"] / 1000000, stats["freq-max"] / 1000000])
    ax.set_xlim([0.0, (stats["time-max"] - float(stats["time-min"]))])
    y2_lower_line = [stats["freq-min"] / 1000000] * len(times)
    ax.fill_between(times, frequencies, y2_lower_line, color="#999999", linewidth=0.0)
    ax.plot(times, frequencies, linewidth=.1)
    ax.set_ylabel("CPU {}".format(v["cpu-id"]))
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.grid(visible=True, which='both', axis='y', linestyle='--', linewidth=.1)
    ax.set_axisbelow(True)
    #ax.yaxis.grid(True)
    #ax.xaxis.set_ticks_position('none')


stats = load_stats()
pprint.pprint(stats)

plt.rcParams.update({'font.size': 5})
fig, axs = plt.subplots(nrows=len(stats["data"]), sharex=True)

for index, (k, v) in enumerate(stats["data"].items()):
    df = df_by_file(v["filename"])
    draw_line(axs[index], df, stats)

plt.subplots_adjust(hspace=.0)
fig.tight_layout(pad=0)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=.2)
image_filename = sys.argv[1] if len(sys.argv) > 1 else "analyze-frequency.pdf"
fig.savefig(image_filename, dpi=DPI, bbox_inches='tight')
print(f"save file as {image_filename}")
