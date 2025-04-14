import subprocess
import os
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker # Import ticker for formatter
import sys
import re
import math

# --- Configuration ---
CPU = "5"
limits = list(range(1, 100))
output_file_prefix = "perf-stat-"
# --- Define events to measure ---
base_events = ['cycles', 'instructions']
cpu_core_events_to_request = [
    'br_misp_retired.all_branches',
    'branch-misses',
    'frontend_retired.latency_ge_1',
    'idq.dsb_cycles_any',
    'idq_bubbles.core',
]
all_events_to_measure = sorted(list(set(base_events + cpu_core_events_to_request)))
events_to_plot_individually = sorted(list(set(cpu_core_events_to_request)))

EVENTS_PER_GROUP = 4
command_checked = False

# --- Helper function to chunk event list ---
def chunk_list(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]

event_groups = list(chunk_list(all_events_to_measure, EVENTS_PER_GROUP))
num_groups = len(event_groups)

# --- Part 0: Cleanup ---
print("--- Cleaning old perf data ---", file=sys.stderr)
cleanup_cmd_str = f"sudo rm -f {output_file_prefix}L*-G*.txt"
subprocess.run(cleanup_cmd_str, shell=True, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# --- Part 1: Run perf stat ---
print(f"Running perf [Core {CPU}] limits {limits[0]}-{limits[-1]}, {num_groups} groups per limit", file=sys.stderr)
total_runs = len(limits) * num_groups
run_count = 0
for limit in limits:
    for group_index, event_group in enumerate(event_groups):
        run_count += 1
        fname = f"{output_file_prefix}L{limit}-G{group_index}.txt"
        cmd = ['sudo', 'perf', 'stat', "-C", CPU, '-j', '--delay', '500', '-o', fname]
        for event in event_group: cmd.extend(['-e', event])
        cmd.extend(['--', 'taskset', "-c", CPU, 'timeout', '5', './dense-switcher', str(limit)])
        print(f"Run {run_count}/{total_runs}", file=sys.stderr, end='\r')
        try:
            subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            command_checked = True
        except FileNotFoundError:
            if not command_checked: print(f"\nError: Required command not found.", file=sys.stderr); sys.exit(1)
            pass
        except Exception as e: print(f"\nError limit {limit}, group {group_index}: {e}", file=sys.stderr); pass
print(f"\n--- Perf runs finished ({run_count} runs) ---", file=sys.stderr)

# --- Part 2: Parse all generated files ---
print("--- Parsing all output files ---", file=sys.stderr)
results = {}

def parse_perf_json_group_file(filename):
    event_data = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip();
                if not line: continue
                try:
                    counter_obj = json.loads(line)
                    if not isinstance(counter_obj, dict): continue
                    event_name_full = counter_obj.get("event")
                    value_str = counter_obj.get("counter-value")
                    if event_name_full and '/' in event_name_full: event_name_base = event_name_full.split('/')[1].rstrip('/')
                    else: event_name_base = event_name_full
                    if event_name_base and value_str is not None:
                        try: event_data[event_name_base.lower()] = float(value_str)
                        except (ValueError, TypeError): pass
                except json.JSONDecodeError: pass
    except FileNotFoundError: return None
    except IOError as e: print(f"Warn: Read Error {filename}: {e}", file=sys.stderr); return None
    return event_data

for limit in limits:
    for group_index in range(num_groups):
        fname = f"{output_file_prefix}L{limit}-G{group_index}.txt"
        parsed_data = parse_perf_json_group_file(fname)
        if parsed_data is not None:
            for event_name_lower, value in parsed_data.items():
                if event_name_lower not in results: results[event_name_lower] = {}
                results[event_name_lower][limit] = value

# --- Part 2.5: Prepare data for plots ---
plot_limits_valid = []
plot_ipc_values = []
plot_event_data = {name: [] for name in events_to_plot_individually}

has_instr = 'instructions' in results
has_cycles = 'cycles' in results
if not (has_instr and has_cycles): print("Error: Missing 'instructions' or 'cycles' data.", file=sys.stderr); sys.exit(1)
instr_data = results['instructions']
cycl_data = results['cycles']

missing_individual_event = False
for event_name in events_to_plot_individually:
    if event_name.lower() not in results: print(f"Warning: Data for event '{event_name}' missing.", file=sys.stderr); missing_individual_event = True
if missing_individual_event: print("Error: Data missing for one or more plot events.", file=sys.stderr); sys.exit(1)

for limit in limits:
    instr = instr_data.get(limit)
    cycl = cycl_data.get(limit)
    if instr is None or cycl is None or cycl <= 0: continue
    current_event_values = {}
    all_present = True
    for event_name in events_to_plot_individually:
        value = results.get(event_name.lower(), {}).get(limit)
        if value is None: all_present = False; break
        current_event_values[event_name] = value
    if all_present:
        plot_limits_valid.append(limit)
        ipc = instr / cycl
        plot_ipc_values.append(ipc)
        for event_name in events_to_plot_individually: plot_event_data[event_name].append(current_event_values[event_name])

if not plot_limits_valid: print("Error: No limits found with complete data. Cannot plot.", file=sys.stderr); sys.exit(1)

# --- Part 3: Plot Data ---
print("--- Plotting results ---", file=sys.stderr)
try:
    import matplotlib.pyplot as plt
    from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
except ImportError: print("Error: matplotlib not installed.", file=sys.stderr); sys.exit(1)

num_plots = 1 + len(events_to_plot_individually)
ncols = 2
nrows = math.ceil(num_plots / ncols)

def prepare_ax(ax, tick_label_size):
    ax.spines['right'].set_visible(False); ax.spines['top'].set_visible(False)
    ax.tick_params(axis='y', labelcolor='0.2', left=False, right=False, labelsize=tick_label_size)
    ax.tick_params(axis='x', labelcolor='0.2', bottom=False, top=False, labelsize=tick_label_size)
    ax.yaxis.grid(True, which='both', linestyle='--', linewidth=0.5, color='darkgray')
    #ax.xaxis.grid(True, which='both', linestyle='--', linewidth=0.5, color='darkgray')
    ax.set_axisbelow(True)

LABEL_FONT_SIZE = 16
TICK_LABEL_FONT_SIZE = 14
SUBPLOT_TITLE_FONT_SIZE = 16

try:
    fig_height = max(4 * nrows, 8)
    fig_width = 20
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, figsize=(fig_width, fig_height), squeeze=False)
    axes_flat = axes.flat
    current_ax_index = 0

    # --- Plot IPC ---
    ax = axes_flat[current_ax_index]
    ax.plot(plot_limits_valid, plot_ipc_values, marker='.', linestyle='-', markersize=3, color='black')
    ax.set_ylabel("IPC", color='0.2', fontsize=LABEL_FONT_SIZE)
    ax.set_title("Instructions Per Cycle (IPC)", fontsize=SUBPLOT_TITLE_FONT_SIZE, color='black')
    ax.set_ylim(bottom=0)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    prepare_ax(ax, TICK_LABEL_FONT_SIZE)
    current_ax_index += 1

    # --- Plot individual events (scaled) ---
    for event_name in events_to_plot_individually:
        if current_ax_index >= len(axes_flat): break
        ax = axes_flat[current_ax_index]
        plot_values_current = plot_event_data[event_name]
        # --- Scale data to millions ---
        plot_values_scaled = [v / 1_000_000.0 for v in plot_values_current]

        ax.plot(plot_limits_valid, plot_values_scaled, marker='.', linestyle='-', markersize=2, color='black')
        # --- Add (Millions) to label ---
        ylabel = "Events [M]"
        ax.set_ylabel(ylabel, color='0.2', fontsize=LABEL_FONT_SIZE)
        ax.set_title(event_name, fontsize=SUBPLOT_TITLE_FONT_SIZE, color='black')
        ax.set_ylim(bottom=0)
        # --- Use non-scientific formatter for scaled values ---
        y_formatter = ScalarFormatter(useOffset=False)
        y_formatter.set_scientific(False)
        ax.yaxis.set_major_formatter(y_formatter)
        prepare_ax(ax, TICK_LABEL_FONT_SIZE)
        current_ax_index += 1

    # --- Post-loop adjustments ---
    start_index_bottom_row = (nrows - 1) * ncols
    # Apply X label and ticks only to plots actually drawn in the bottom row
    for i in range(start_index_bottom_row, num_plots):
         ax = axes_flat[i]
         ax.set_xlabel("Limit Argument [#]", color='0.2', fontsize=LABEL_FONT_SIZE)
         ax.tick_params(axis='x', bottom=True, top=False, labelsize=TICK_LABEL_FONT_SIZE)
         tick_step = max(1, len(plot_limits_valid) // 10)
         ax.set_xticks(plot_limits_valid[::tick_step])

    # Hide unused axes
    for i in range(num_plots, nrows * ncols):
         fig.delaxes(axes_flat[i])

    fig.tight_layout(pad=2.0, h_pad=3.0, w_pad=3.0)

    # --- Save ---
    plot_filename = "selected-events-scaled-vs-limit.pdf" # Updated name
    fig.savefig(plot_filename, format="pdf", transparent=False)
    print(f"Plot saved to {plot_filename}", file=sys.stderr)

except Exception as e:
    print(f"Error during plotting/saving: {e}", file=sys.stderr)
    sys.exit(1)

print("Script finished.", file=sys.stderr)
