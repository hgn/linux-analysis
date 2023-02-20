#!/usr/bin/python3

import sys
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import json
from cycler import cycler
import copy

#plt.style.use('grayscale')
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
    lables = []
    for state, state_data in db.items():
        lables.append(state)
        times.append(state_data)
    return lables, times



def graph_pie_by_time(db, pdfname):
    labels, times = transform_data(db)

    #colors = plt.cm.gray(np.linspace(0.2,0.8,5))
    #plt.rcParams['axes.prop_cycle'] = cycler(color=colors)

    fig, ax = plt.subplots()
    fig.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    ax.margins(0, 0)
    patches, texts = ax.pie(times)
    nd_times = np.array(times)
    porcent = 100.*nd_times/nd_times.sum()
    pie_labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(labels, porcent)]
    patches, pie_labels, dummy =  zip(*sorted(zip(patches, pie_labels, nd_times), key=lambda x: x[2], reverse=True))
    fig.legend(patches, pie_labels, loc='upper left', fontsize=10)
    image_filename = pdfname
    fig.savefig(image_filename, dpi=DPI, transparent=True, bbox_inches='tight')
    print(f"save file as {image_filename}")


files = [
    ["cpu-idle-idle.json", "c-states-by-time-idle.png" ],
    ["cpu-idle-j-nproc.json", "c-states-by-time-j-nproc.png" ],
    ["cpu-idle-j-64.json", "c-states-by-time-j-64.png" ]
    ]
for filename, pdf_name in files:
    db = load_json_file(filename)
    graph_pie_by_time(db, pdf_name)
