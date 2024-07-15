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
    usages = []
    lables = []
    for state, state_data in db["all"].items():
        lables.append(state_data["name"])
        times.append(state_data["time"])
        usages.append(state_data["usage"])
    return lables, times, usages


db = load_json_file(sys.argv[1])

def graph_pie_by_time():
    labels, times, usages = transform_data(db)

    #colors = plt.cm.gray(np.linspace(0.2,0.8,5))
    #plt.rcParams['axes.prop_cycle'] = cycler(color=colors)

    fig, ax = plt.subplots()
    patches, texts = ax.pie(times)
    nd_times = np.array(times)
    porcent = 100.*nd_times/nd_times.sum()
    pie_labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(labels, porcent)]
    patches, pie_labels, dummy =  zip(*sorted(zip(patches, pie_labels, nd_times), key=lambda x: x[2], reverse=True))
    fig.legend(patches, pie_labels, loc='center left', fontsize=10)
    image_filename = "c-states-by-time.pdf"
    fig.savefig(image_filename, dpi=DPI, bbox_inches='tight')
    print(f"save file as {image_filename}")

def graph_pie_by_usage():
    labels, times, usages = transform_data(db)

    #colors = plt.cm.gray(np.linspace(0.2,0.8,5))
    #plt.rcParams['axes.prop_cycle'] = cycler(color=colors)

    fig, ax = plt.subplots()
    patches, texts = ax.pie(usages)
    nd_times = np.array(usages)
    porcent = 100.*nd_times/nd_times.sum()
    pie_labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(labels, porcent)]
    patches, pie_labels, dummy =  zip(*sorted(zip(patches, pie_labels, nd_times), key=lambda x: x[2], reverse=True))
    fig.legend(patches, pie_labels, loc='center left', fontsize=10)
    image_filename = "c-states-by-usage.pdf"
    fig.savefig(image_filename, dpi=DPI, bbox_inches='tight')
    print(f"save file as {image_filename}")

def stacked_bar_transform_data_time(db):
    cpus = []
    keys = {}
    for k, v in db["all"].items():
        name = v["name"]
        if name not in keys:
            keys[name] = np.array([])
    db = copy.deepcopy(db)
    del db['all']
    for cpu, cpu_data in sorted(db.items(),  key=lambda item: int(item[0])):
        cpus.append(cpu)
        for k, v in cpu_data.items():
            keys[v["name"]] = np.append(keys[v["name"]], v["time"])
    return cpus, keys

def stacked_bar_transform_data_usage(db):
    cpus = []
    keys = {}
    for k, v in db["all"].items():
        name = v["name"]
        if name not in keys:
            keys[name] = np.array([])
    db = copy.deepcopy(db)
    del db['all']
    for cpu, cpu_data in sorted(db.items(),  key=lambda item: int(item[0])):
        cpus.append(cpu)
        for k, v in cpu_data.items():
            keys[v["name"]] = np.append(keys[v["name"]], v["usage"])
    return cpus, keys

def graph_stacked_bar_by_time():
    colors=['darkgray','gray','dimgray','lightgray']
    cpus, data = stacked_bar_transform_data_time(db)
    width = 0.4
    fig, ax = plt.subplots()
    bottom = np.zeros(len(cpus))
    for boolean, weight_count in data.items():
        p = ax.bar(cpus, weight_count, width, label=boolean, bottom=bottom)
        bottom += weight_count
    plt.xticks(fontsize=12, rotation=40)
    #ax.axes.get_yaxis().set_visible(False)
    ax.set_ylabel('C-States Time Accumulated [s]')
    ax.set_yticklabels([])


    ax.tick_params(axis="x", labelsize=8)
    ax.set_xlabel('CPU Hardware Thread ID')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])

    image_filename = "c-states-by-time-by-thread.pdf"
    fig.savefig(image_filename, dpi=DPI, bbox_inches='tight')
    print(f"save file as {image_filename}")

def graph_stacked_bar_by_usage():
    colors=['darkgray','gray','dimgray','lightgray']
    cpus, data = stacked_bar_transform_data_usage(db)
    width = 0.4
    fig, ax = plt.subplots()
    bottom = np.zeros(len(cpus))
    for boolean, weight_count in data.items():
        p = ax.bar(cpus, weight_count, width, label=boolean, bottom=bottom)
        bottom += weight_count
    plt.xticks(fontsize=12, rotation=40)
    #ax.axes.get_yaxis().set_visible(False)
    ax.set_ylabel('C-States Usage [Calls]')
    ax.set_yticklabels([])


    ax.tick_params(axis="x", labelsize=8)
    ax.set_xlabel('CPU Hardware Thread ID')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])

    image_filename = "c-states-by-usage-by-thread.pdf"
    fig.savefig(image_filename, dpi=DPI, bbox_inches='tight')
    print(f"save file as {image_filename}")

graph_pie_by_time()
graph_pie_by_usage()
graph_stacked_bar_by_time()
graph_stacked_bar_by_usage()
