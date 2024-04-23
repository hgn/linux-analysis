#!/usr/bin/env python3

import matplotlib.pyplot as plt
import re

def parse_data(filename):
  """
  Parses data from the given file and returns a dictionary with CPU data.

  Args:
      filename: The path to the data file.

  Returns:
      A dictionary where keys are CPU numbers and values are lists of tuples
      containing timestamps and TSC values.
  """
  cpu_data = {}
  with open(filename, "r") as f:
    for line in f.readlines():
      if line.startswith("CPU"):
        cpu_number = int(re.findall(r"CPU (\d+)", line)[0])
        cpu_data[cpu_number] = []
      else:
        # Check if the pattern is found before accessing index
        match = re.search(r"timestamp:(\d+\.\d+);tsc:(\d+)", line)
        if match:
          timestamp, tsc = map(float, match.groups())
          cpu_data[cpu_number].append((timestamp, tsc))
  return cpu_data

def plot_data(cpu_data):
  """
  Plots data for each CPU in a separate line graph using Matplotlib's
  object-oriented interface.

  Args:
      cpu_data: A dictionary containing CPU data as parsed by the `parse_data` function.
  """
  fig, ax = plt.subplots()
  for cpu_number, data in cpu_data.items():
    timestamps, tsc_values = zip(*data)
    ax.plot(timestamps, tsc_values, label=f"CPU {cpu_number}")

  ax.set_xlabel("Timestamp (seconds)")
  ax.set_ylabel("TSC Value")
  ax.set_title("TSC Values vs Time per CPU")
  ax.legend()
  plt.show()

# Parse data from the file
cpu_data = parse_data("constant-rtc.log")

# Plot the data
plot_data(cpu_data)

