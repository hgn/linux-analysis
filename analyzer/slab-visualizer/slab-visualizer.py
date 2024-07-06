#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

DPI = 300
FIGSIZE_WIDE = (18, 7)

plt.rcParams.update({'font.size': 14})

class SlabInfoParser:
    def __init__(self, filepath='/proc/slabinfo'):
        self.filepath = filepath
        self.slab_data = {}

    def parse(self):
        with open(self.filepath, 'r') as file:
            lines = file.readlines()
            headers = lines[0].split()
            for line in lines[2:]:  # Skip the first two lines
                parts = line.split()
                if len(parts) < len(headers):
                    continue
                name = parts[0]
                active_objs = int(parts[1])
                num_objs = int(parts[2])
                obj_size = int(parts[3])
                slabs = int(parts[4])
                self.slab_data[name] = {
                    'active_objs_bytes': active_objs * obj_size,
                    'num_objs_bytes': num_objs * obj_size,
                    'obj_size': obj_size,
                    'slabs': slabs
                }

    def get_slab_data(self):
        return self.slab_data

class SlabInfoPlotter:
    def __init__(self, slab_data):
        self.slab_data = slab_data

    def plot(self):
        sorted_slab_data = sorted(self.slab_data.items(), key=lambda item: item[1]['num_objs_bytes'], reverse=True)
        top_slab_data = sorted_slab_data[:20]

        names = [item[0] for item in top_slab_data]
        active_objs_bytes = [item[1]['active_objs_bytes'] for item in top_slab_data]
        num_objs_bytes = [item[1]['num_objs_bytes'] for item in top_slab_data]

        x = np.arange(len(names))  # the label locations
        width = 0.35  # the width of the bars

        print("{} {}\n".format(active_objs_bytes, num_objs_bytes))

        fig, ax = plt.subplots()
        bars1 = ax.bar(x - width/2, active_objs_bytes, width, label='Active Objects Bytes')
        bars2 = ax.bar(x + width/2, num_objs_bytes, width, label='Total Objects Bytes')

        ax.set_xlabel('Slab Names')
        ax.set_ylabel('Size in Bytes')
        ax.set_title('Top 20 Slabs by Size in Bytes')
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, fontsize=14, ha='right')
        ax.legend()

        ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))

        fig.tight_layout()
        fig.savefig('slabs-visualized.pdf', dpi=DPI, bbox_inches='tight')
        print("Save file slabs-visualied.pdf")

if __name__ == "__main__":
    parser = SlabInfoParser()
    parser.parse()
    slab_data = parser.get_slab_data()

    plotter = SlabInfoPlotter(slab_data)
    plotter.plot()

