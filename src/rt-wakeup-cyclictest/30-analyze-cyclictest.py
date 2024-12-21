import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def read_histogram_files(histogram_prefix, cores):
    data = {}
    for core in range(1, cores + 1):
        histogram_file = f"{histogram_prefix}{core}"
        core_data = pd.read_csv(histogram_file, sep="\t", header=None, names=["Latency", f"Core {core - 1}"])
        data[f"Core {core - 1}"] = core_data
    return data

def prepare_ax(ax):
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(top=False)
    ax.tick_params(left=False)
    ax.tick_params(bottom=False)
    ax.tick_params(axis='y', labelcolor='0.2')
    ax.yaxis.grid(True, which='both', linestyle='--', linewidth=0.5, color='lightgray')
    ax.xaxis.grid(True, which='both', linestyle='--', linewidth=0.5, color='lightgray')
    ax.set_axisbelow(True)

def plot_latency_histogram(data, max_latency, output_image):
    fig, ax = plt.subplots(figsize=(17, 7), dpi=300)
    prepare_ax(ax)

    for core_data in data.values():
        ax.fill_between(core_data["Latency"], core_data.iloc[:, 1], color='gray', alpha=0.4)
        ax.plot(core_data["Latency"], core_data.iloc[:, 1], color='gray', alpha=0.7)
    
    ax.tick_params(axis='x', which='both', bottom=True, labelbottom=True)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}"))

    ax.set_xlabel("Latency [us]", fontsize=14)
    ax.set_ylabel("Number Samples [#]", fontsize=14)
    ax.set_yscale("log")
    ax.set_xscale("log")
    #ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}"))
    #ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}"))
    fig.tight_layout()
    fig.savefig(output_image, format="pdf", transparent=False, bbox_inches="tight")
    print(f"Saved plot to {output_image}")

def main():
    histogram_prefix = "histogram"
    cores = os.cpu_count()
    max_latency = 400
    output_image = "30-analyze-cyclictest.pdf"

    data = read_histogram_files(histogram_prefix, cores)
    plot_latency_histogram(data, max_latency, output_image)

if __name__ == "__main__":
    main()

