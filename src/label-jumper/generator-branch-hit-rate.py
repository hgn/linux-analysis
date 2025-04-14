import subprocess
import os
import json
import matplotlib.pyplot as plt
import sys

CPU = "5"
limits = list(range(1, 50))
output_file_prefix = "perf-stat-"
perf_events_str = 'cycles,instructions,branches,branch-misses,baclears.any'
branches_event_name = "cpu_core/branches/"
misses_event_name = "cpu_core/branch-misses/"
command_checked = False

cleanup_cmd_str = f"sudo rm -f {output_file_prefix}*.txt"
subprocess.run(cleanup_cmd_str, shell=True, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Minimal status prints retained
print(f"Running perf [Core {CPU}] limits {limits[0]}-{limits[-1]}", file=sys.stderr)
for limit in limits:
    fname = f"{output_file_prefix}{limit}.txt"
    cmd = [
        'sudo', 'perf', 'stat', "-C", CPU, '-j', '-o', fname,
        '-e', perf_events_str,
        '--', 'taskset', "-c", CPU, 'timeout', '5', './dense-switcher', str(limit)
    ]
    print(f"Run limit {limit}", file=sys.stderr, end='\r')
    try:
        subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        command_checked = True
    except FileNotFoundError:
        if not command_checked:
             print(f"\nError: Required command not found.", file=sys.stderr)
             sys.exit(1)
        pass
    except Exception as e:
        print(f"\nError limit {limit}: {e}", file=sys.stderr)
        pass
print("\nPerf runs finished.", file=sys.stderr)


plot_limits = []
plot_hit_rates = []

def parse_perf_json_linewise(filename, branches_key, misses_key):
    branches_val = None
    misses_val = None
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                try:
                    counter_obj = json.loads(line)
                    if not isinstance(counter_obj, dict): continue
                    event_name = counter_obj.get("event")
                    value_str = counter_obj.get("counter-value")
                    current_val = None
                    if value_str is not None:
                        try: current_val = float(value_str)
                        except (ValueError, TypeError): continue
                    if event_name == branches_key: branches_val = current_val
                    elif event_name == misses_key: misses_val = current_val
                    if branches_val is not None and misses_val is not None: break
                except json.JSONDecodeError:
                    pass
    except FileNotFoundError: return None, None
    except IOError as e:
        print(f"Warn: Read Error {filename}: {e}", file=sys.stderr)
        return None, None
    return branches_val, misses_val

for limit in limits:
    fname = f"{output_file_prefix}{limit}.txt"
    try:
        branches_count, misses_count = parse_perf_json_linewise(fname, branches_event_name, misses_event_name)
        if branches_count is not None and misses_count is not None:
            if branches_count > 0:
                actual_misses = min(misses_count, branches_count)
                if actual_misses < 0: actual_misses = 0
                hit_rate = ((branches_count - actual_misses) / branches_count) * 100.0
            else:
                hit_rate = 100.0
            plot_limits.append(limit)
            plot_hit_rates.append(hit_rate)
    except Exception as e:
         print(f"Warn: Error processing data for limit {limit}: {e}", file=sys.stderr)
         pass

if not plot_limits:
    print("Error: No valid data parsed. Cannot plot.", file=sys.stderr)
    sys.exit(1)

def prepare_ax(ax, tick_label_size):
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(axis='y', labelcolor='0.2', left=False, right=False, labelsize=tick_label_size)
    ax.tick_params(axis='x', labelcolor='0.2', bottom=False, top=False, labelsize=tick_label_size)
    ax.yaxis.grid(True, which='both', linestyle='--', linewidth=0.5, color='darkgray') # Slightly darker grid
    #ax.xaxis.grid(True, which='both', linestyle='-', linewidth=0.2, color='darkgray')
    ax.set_axisbelow(True)

try:
    # --- Font Size Configuration ---
    TITLE_FONT_SIZE = 18
    LABEL_FONT_SIZE = 17
    TICK_LABEL_FONT_SIZE = 14

    fig, ax = plt.subplots(figsize=(15, 7))

    # Plot data using the axes object - black color for grayscale
    ax.plot(plot_limits, plot_hit_rates, marker='.', linestyle='-', markersize=3, color='black')

    # Set labels and title using axes object methods - added fontsize
    ax.set_xlabel("Limit Argument [#]", color='0.2', fontsize=LABEL_FONT_SIZE)
    ax.set_ylabel("Branch Prediction Hit Rate [%]", color='0.2', fontsize=LABEL_FONT_SIZE)

    # Set axis limits
    ax.set_ylim(bottom=0, top=101)

    # Set and rotate x-ticks
    tick_step = max(1, len(plot_limits) // 20)
    ax.set_xticks(plot_limits[::tick_step])
    # Rotation is handled by tick_params within prepare_ax now or separate? Separate is fine.
    ax.tick_params(axis='x')

    # Apply the custom styling via the function AFTER basic setup
    prepare_ax(ax, TICK_LABEL_FONT_SIZE)

    # Define PDF filename and save
    plot_filename = "branch-hit-rate-vs-limit.pdf"
    fig.savefig(plot_filename, format="pdf", transparent=False, bbox_inches="tight")
    print(f"Plot saved to {plot_filename}", file=sys.stderr)

except ImportError:
    print("Error: matplotlib not installed. Cannot plot.", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error during plotting/saving: {e}", file=sys.stderr)
    sys.exit(1)

print("Script finished.", file=sys.stderr) # Minimal final message
