#!/usr/bin/python3

import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib

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

def load_csv_file(filename):
    return pd.read_csv(filename, sep=";", header=0, on_bad_lines='warn')

df_temp = load_csv_file("log-temperature.csv")
df_usage = load_csv_file("log-usage.csv")

entries = list(df_temp.columns)[1:]
fig, ax = plt.subplots(figsize=FIGSIZE_WIDE, nrows=len(entries), ncols=2, sharex=False)

colormap = "YlOrRd"
colormap = "Greys"

for i, entry in enumerate(entries, start=0):
    prepare_ax(ax[i][1])
    a = np.array(list(df_usage[entry]))
    ax[i][0].imshow(np.expand_dims(a, axis=0), aspect='auto', cmap=colormap, vmin=-100, vmax=100)
    ax[i][0].set_ylabel(f"Core {entry}", fontsize=4, rotation=0, va="center")

    prepare_ax(ax[i][0])
    a = np.array(list(df_temp[entry]))
    ax[i][1].imshow(np.expand_dims(a, axis=0), aspect='auto', cmap=colormap, vmin=60, vmax=100)
    ax[i][1].set_ylabel(f"Core {entry}", fontsize=4, rotation=0, va="center")

axs = ax.flatten()[:2]
axs[0].axis("off")
axs[0].set_title("Core Usage", fontsize=6)
axs[1].axis("off")
axs[1].set_title("Core Temperature", fontsize=6)

image_filename = sys.argv[1] if len(sys.argv) > 1 else "graph.pdf"
fig.savefig(image_filename, dpi=DPI, bbox_inches='tight')
print(f"save file as {image_filename}")
