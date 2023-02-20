#!/usr/bin/python3

import os
import sys
import pathlib



import numpy as np
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


root_dir = os.path.abspath(os.path.dirname(__file__))

trans_tbl = pathlib.Path("/sys/devices/system/cpu/cpu0/cpufreq/stats/trans_table")
if not trans_tbl.is_file():
    print(f"file {trans_tbl} not available,", end='')
    print(" probably wrong cpu scaling governor - need acpi")
    sys.exit(1)

# simple strip out header from raw trans_table
trans_tbl_data = trans_tbl.read_text().splitlines()
freqs_hz = list(map(int, trans_tbl_data[1].split()[1:]))
freqs_y = [x // 1000 for x in freqs_hz]
freqs_x = list(reversed(freqs_y))

plot_data = []
for line in trans_tbl_data[2:]:
    entries = list(reversed(line.split()[1:]))
    plot_data.append(list(map(int, entries)))


harvest = np.array(plot_data)


fig, ax = plt.subplots()
im = ax.imshow(harvest, cmap='gray_r', norm=LogNorm())

# Show all ticks and label them with the respective list entries
ax.set_xticks(np.arange(len(freqs_x)), labels=freqs_x)
ax.set_yticks(np.arange(len(freqs_y)), labels=freqs_y)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(freqs_x)):
    for j in range(len(freqs_y)):
        text = ax.text(j, i, harvest[i, j], ha="center", va="center", color="w")

plt.xlabel('To [kHz]')
plt.ylabel('From [kHz]')

fig.tight_layout()
plt.show()










