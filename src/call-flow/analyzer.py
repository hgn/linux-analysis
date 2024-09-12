#!/usr/bin/env python3

import subprocess
import re
from collections import defaultdict, OrderedDict

# Section 1: Parse 'perf-sched-switch.data' for sched_switch events

def parse_sched_switch(output):
    """
    Parses the perf script output and extracts the timestamps for when 'call-flow-examp'
    is switched in and out, using nanosecond precision.

    Returns two ordered lists: one for switch-in times and one for switch-out times.
    """
    switch_in_times = []
    switch_out_times = []

    # Regex patterns for detecting switch-in and switch-out events
    switch_in_pattern = re.compile(
        r'.* \[\d+\] (\d+\.\d+): sched:sched_switch: .* ==> call-flow-examp:\d+'
    )
    switch_out_pattern = re.compile(
        r'.* \[\d+\] (\d+\.\d+): sched:sched_switch: call-flow-examp:\d+.* ==> .*'
    )

    for line in output.splitlines():
        match_in = switch_in_pattern.search(line)
        match_out = switch_out_pattern.search(line)

        if match_in:
            switch_in_times.append(float(match_in.group(1)))
        if match_out:
            switch_out_times.append(float(match_out.group(1)))

    return switch_in_times, switch_out_times

# Section 2: Parse 'perf.data' for syscalls and cycle samples

def parse_syscalls_and_cycles(output):
    """
    Parses the perf script output to record syscalls and function samples with call graphs.

    Returns:
    - syscalls_dict: A dictionary with timestamps as keys and details of syscalls.
    - cycle_samples: A dictionary with function names as keys and their call graph & hotness.
    """
    syscalls_dict = OrderedDict()
    cycle_samples = defaultdict(lambda: {"count": 0, "call_graphs": []})
    pending_syscalls = {}  # Track syscalls that are entered but not yet exited

    # Adjusted Regex patterns
    syscall_pattern = re.compile(r'call-flow-examp.* (\d+\.\d+):\s+syscalls:(sys_enter|sys_exit)_(\w+):\s+(.*)')
    cycle_pattern = re.compile(r'call-flow-examp.* (\d+\.\d+):\s+\d+\s+cpu_core/cycles/u:')
    function_pattern = re.compile(r'\s+(\S+)\s+\+\S+\s+\(.+\)')

    current_call_graph = []
    capturing_call_graph = False

    for line in output.splitlines():
        syscall_match = syscall_pattern.search(line)
        cycle_match = cycle_pattern.search(line)

        if syscall_match:
            timestamp, syscall_type, syscall_name, details = syscall_match.groups()
            timestamp = float(timestamp)

            if syscall_type == "sys_enter":
                pending_syscalls[timestamp] = syscall_name  # Track entered syscalls

            elif syscall_type == "sys_exit" and pending_syscalls:
                # Find the closest matching enter for this exit
                closest_enter_time = max(t for t in pending_syscalls.keys() if t <= timestamp)
                entry_exit = {
                    "type": "exit",
                    "name": syscall_name,
                    "details": details,
                    "enter_time": closest_enter_time,
                }
                syscalls_dict[closest_enter_time] = entry_exit
                del pending_syscalls[closest_enter_time]

            # Reset call graph for the next syscall or cycle
            current_call_graph = []
            capturing_call_graph = False

        elif cycle_match:
            timestamp = float(cycle_match.group(1))
            capturing_call_graph = True  # Start capturing call graph for the cycle sample

            # Reset call graph for this cycle sample
            current_call_graph = []

        elif capturing_call_graph:
            function_match = function_pattern.search(line)
            if function_match:
                function_name = function_match.group(1)
                current_call_graph.append(function_name)
                cycle_samples[function_name]["count"] += 1
                cycle_samples[function_name]["call_graphs"].append(current_call_graph.copy())

    return syscalls_dict, cycle_samples, pending_syscalls

# Section 3: Utility function to run 'perf script' and capture the output

def run_perf_script(perf_data_file):
    """
    Runs the 'perf script' command with nanosecond precision and captures the output.

    Returns the output of the command.
    """
    try:
        result = subprocess.run(
            ['perf', 'script', '--ns', '-i', perf_data_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running perf script: {e.stderr}")
        raise

# Section 4: Correlate syscalls with schedule in/out events

def correlate_syscalls_with_sched(switch_in_times, switch_out_times, syscalls_dict, pending_syscalls):
    """
    Correlates syscalls with the times when 'call-flow-examp' was scheduled in and out.

    For each schedule-in, find the first syscall exit.
    For each schedule-out, find the last syscall enter that didn't have an exit.
    """
    first_syscall_exits_after_in = []
    unpaired_syscall_enters_before_out = []

    for sched_in_time in switch_in_times:
        # Find the first syscall exit after this schedule-in time
        first_exit = next((details["name"] for time, details in syscalls_dict.items() if time > sched_in_time and details["type"] == "exit"), None)
        if first_exit:
            first_syscall_exits_after_in.append((sched_in_time, first_exit))

    for sched_out_time in switch_out_times:
        # Find syscalls that were entered but did not exit before this schedule-out time
        unpaired_enters = [syscall_name for time, syscall_name in pending_syscalls.items() if time < sched_out_time]
        if unpaired_enters:
            unpaired_syscall_enters_before_out.append((sched_out_time, unpaired_enters))

    return first_syscall_exits_after_in, unpaired_syscall_enters_before_out

# Section 5: Main function to coordinate the analysis

def main():
    # Analyzing 'perf-sched-switch.data'
    perf_sched_data_file = 'perf-sched-switch.data'
    try:
        sched_output = run_perf_script(perf_sched_data_file)
    except Exception as e:
        print(f"Failed to run perf script on {perf_sched_data_file}: {e}")
        return

    switch_in_times, switch_out_times = parse_sched_switch(sched_output)

    # Analyzing 'perf.data'
    perf_data_file = 'perf.data'
    try:
        perf_output = run_perf_script(perf_data_file)
    except Exception as e:
        print(f"Failed to run perf script on {perf_data_file}: {e}")
        return

    syscalls_dict, cycle_samples, pending_syscalls = parse_syscalls_and_cycles(perf_output)

    # Correlate syscalls with schedule in/out events
    first_syscall_exits_after_in, unpaired_syscall_enters_before_out = correlate_syscalls_with_sched(
        switch_in_times, switch_out_times, syscalls_dict, pending_syscalls
    )

    # Print results
    print("First syscall exits after each schedule-in:")
    for sched_in_time, syscall_name in first_syscall_exits_after_in:
        print(f"  Schedule-in time: {sched_in_time} ns - First syscall exit: {syscall_name}")

    print("\nUnpaired syscall enters before each schedule-out:")
    for sched_out_time, unpaired_syscalls in unpaired_syscall_enters_before_out:
        print(f"  Schedule-out time: {sched_out_time} ns - Unpaired syscall enters: {', '.join(unpaired_syscalls)}")

if __name__ == "__main__":
    main()

