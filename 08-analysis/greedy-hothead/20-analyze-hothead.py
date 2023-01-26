#!/usr/bin/python3

import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
from matplotlib.colors import LogNorm
import matplotlib.colors as mcolors
from matplotlib.patches import Polygon
from itertools import cycle


plt.style.use('grayscale')
DPI=300
FIGSIZE_WIDE = (12,12)

def load_stats():
    with open(stats_path) as fd:
        return json.load(fd)

def load_df_file(filename):
    df = pd.read_csv(filename, names= ['time','package', 'core', 'uncore'], sep=";", skiprows=1)
    #df = df.astype({'time':'float','frequency':'int'})
    #df["frequency"] = df["frequency"].div(1000000)
    return df

def load_df_temp_file(filename):
    df = pd.read_csv(filename, sep=";", header=0)
    #df = df.astype({'time':'float','frequency':'int'})
    #df["frequency"] = df["frequency"].div(1000000)
    return df


def prepare_ax(ax):
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

def prepare_map(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

def gradient_fill(x, y, fill_color=None, ax=None, **kwargs):
    """
    Plot a line with a linear alpha gradient filled beneath it.

    Parameters
    ----------
    x, y : array-like
        The data values of the line.
    fill_color : a matplotlib color specifier (string, tuple) or None
        The color for the fill. If None, the color of the line will be used.
    ax : a matplotlib Axes instance
        The axes to plot on. If None, the current pyplot axes will be used.
    Additional arguments are passed on to matplotlib's ``plot`` function.

    Returns
    -------
    line : a Line2D instance
        The line plotted.
    im : an AxesImage instance
        The transparent gradient clipped to just the area beneath the curve.
    """
    if ax is None:
        ax = plt.gca()

    line, = ax.plot(x, y, **kwargs, linewidth=.01)
    if fill_color is None:
        fill_color = line.get_color()

    zorder = line.get_zorder()
    alpha = line.get_alpha()
    alpha = 1.0 if alpha is None else alpha

    z = np.empty((100, 1, 4), dtype=float)
    rgb = mcolors.colorConverter.to_rgb(fill_color)
    z[:,:,:3] = rgb
    z[:,:,-1] = np.linspace(0, alpha, 100)[:,None]

    xmin, xmax, ymin, ymax = x.min(), x.max(), y.min(), y.max()
    im = ax.imshow(z, aspect='auto', extent=[xmin, xmax, ymin, ymax],
                   origin='lower', zorder=zorder)

    xy = np.column_stack([x, y])
    xy = np.vstack([[xmin, ymin], xy, [xmax, ymin], [xmin, ymin]])
    clip_path = Polygon(xy, facecolor='none', edgecolor='none', closed=True, linewidth=.01)
    ax.add_patch(clip_path)
    im.set_clip_path(clip_path)

    ax.autoscale(True)
    return line, im





df = pd.read_csv("freq-log.csv", sep=";", on_bad_lines='warn')
del df[df.columns[0]]
#for index, row in df.iterrows():vmin=0., vmax=100.
#    print(row)

#column_labels = list('ABCD')
#row_labels = list('WXYZ')
df_eff = df.iloc[:, 16:32]

df_perf = df.iloc[:, 0:16]


plt.rcParams.update({'font.size': 10})
fig, (ax1, ax2, ax3, ax4) = plt.subplots(figsize=FIGSIZE_WIDE, nrows=4, sharex=True, constrained_layout=True)


prepare_ax(ax1)
prepare_ax(ax4)
prepare_map(ax2)
prepare_map(ax3)




dfx = load_df_file("power-log.csv")
#gradient_fill(dfx["time"], dfx["package"], ax=ax1)
ax1.plot(dfx["time"], dfx["package"], label="Package", linewidth=1.)
ax1.plot(dfx["time"], dfx["uncore"], label="Uncore", linewidth=1.)
ax1.legend(fontsize=9, frameon=False, loc='upper right')
ax1.set_ylabel("Power [Watt]")
ax1.set_title("Power Consumption")





# efficiency cores
cmap = "binary" # 'YlOrRd'
im1 = ax2.pcolor(df_eff.transpose(), cmap=cmap, vmin=4000., vmax=4500.)
fig.colorbar(im1, ax=ax2)
ax2.set_yticklabels(list(range(17,33*2)))
ax2.set_title("Core Frequency")
ax2.set_ylabel("Efficency Cores [Hz]")

# performacne cores
im2 = ax3.pcolor(df_perf.transpose(), cmap=cmap, vmin=5000., vmax=5500.)
fig.colorbar(im2, ax=ax3)
ax3.set_ylabel("Performance Cores [Hz]")

lines = ["k-","k--","k-.","k:"]
linecycler = cycle(lines)
df_temp = load_df_temp_file("temp-log.csv")
entries = list(df_temp.columns)[1:]
ax4.set_title("Core Temperature")
for entrie in entries:
    ax4.plot(df_temp[["time"]], df_temp[[entrie]], next(linecycler), label=entrie, linewidth=.7)
    ax4.legend(fontsize=9, frameon=False, ncol=3, loc='lower center')
    ax4.set_ylabel("Temperature [$^\circ$C]")
#for index, row in df_temp.iterrows():
 #   print(row)
#for (columnName, columnData) in stu_df.iteritems():
#print(df_temp)
#ax4.plot(df_temp["time"], df_temp["temp"], linewidth=1.)

# put the major ticks at the middle of each cell
#ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)
#ax.set_yticks(np.arange(data.shape[0]) + 0.5, minor=False)

# want a more natural, table-like display
#ax.invert_yaxis()
#ax.xaxis.tick_top()

#ax.set_xticklabels(column_labels, minor=False)
#ax.set_yticklabels(row_labels, minor=False)
image_filename = sys.argv[1] if len(sys.argv) > 1 else "graph.pdf"
fig.savefig(image_filename, dpi=DPI, bbox_inches='tight')
print(f"save file as {image_filename}")
